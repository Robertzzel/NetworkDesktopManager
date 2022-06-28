package main

import (
	"errors"
	"fmt"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"

	"example.com/orchestrators/communication"
	"example.com/orchestrators/pathlib"
	zmq "github.com/pebbe/zmq4"
)

var EnvInterpretorPath = pathlib.GetCurrentPath().GetParent().GetParent().GetParent().Add("venv").Add("bin").Add("python3")

const padding = 10

type Client struct {
	loggerFile            *os.File
	ServerAddress         string
	imageDisplayerAddress string
	SocketServer          communication.TCPConnection
	SocketImageDisplayer  *zmq.Socket
	SocketSoundPlayer     *zmq.Socket
	SocketInputGenerator  *zmq.Socket
	Processes             []*os.Process
	isRunning             bool
}

func NewClient(serverAddress string, imageDisplayerAddress string, loggerFile *os.File) (Client, error) {
	context, _ := zmq.NewContext()
	socketImageDisplayer, _ := context.NewSocket(zmq.PAIR)
	socketSoundPlayer, _ := context.NewSocket(zmq.PUSH)
	socketInputGenerator, _ := context.NewSocket(zmq.PULL)

	return Client{
		loggerFile:            loggerFile,
		imageDisplayerAddress: imageDisplayerAddress,
		ServerAddress:         serverAddress,
		SocketImageDisplayer:  socketImageDisplayer,
		SocketSoundPlayer:     socketSoundPlayer,
		SocketInputGenerator:  socketInputGenerator,
		isRunning:             false,
		SocketServer:          communication.TCPConnection{},
	}, nil
}

func (cl *Client) Start() {
	cl.SocketImageDisplayer.Connect(fmt.Sprintf("tcp://%s", cl.imageDisplayerAddress))
	cl.SocketSoundPlayer.Bind("tcp://*:6111")
	cl.SocketInputGenerator.Bind("tcp://*:6222")

	cl.loggerFile.Write([]byte("Connecting to server..\n"))
	connection, err := net.Dial("tcp", cl.ServerAddress)
	if err != nil {
		cl.loggerFile.Write([]byte(fmt.Sprintf("Cannot connect to server %s", err)))
		cl.Stop()
		return
	}
	cl.SocketServer = communication.TCPConnection{connection}
	cl.loggerFile.Write([]byte("Connected...\n"))

	cl.isRunning = true

	if err := cl.startProcesses(); err != nil {
		cl.loggerFile.Write([]byte(fmt.Sprintln(err)))
		cl.Stop()
		return
	}

	cl.routeMessages()
}

func (cl *Client) startProcesses() error {
	basePath := pathlib.GetCurrentPath().GetParent().GetParent().GetParent()
	soundPlayerPath := basePath.Add("Consumers").Add("sound_player.py")
	inputGeneratorPath := basePath.Add("Producers").Add("input_generator.py")

	if !EnvInterpretorPath.FileExists() {
		return errors.New("enviroment path does not exist")
	}
	if !soundPlayerPath.FileExists() || !inputGeneratorPath.FileExists() {
		return errors.New("processes cannot be open, one of the file does not exists")
	}

	cl.Processes = append(cl.Processes, startPythonProcess([]string{soundPlayerPath.ToString(), "6111"}))
	cl.Processes = append(cl.Processes, startPythonProcess([]string{inputGeneratorPath.ToString(), "6222"}))

	return nil
}

func startPythonProcess(argv []string) *os.Process {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)
	cmd.Start()
	return cmd.Process
}

func (cl *Client) routeMessages() {
	defer cl.Stop()
	go cl.receiveImagesAndAudio()

	poller := zmq.NewPoller()
	poller.Add(cl.SocketInputGenerator, zmq.POLLIN)

	for cl.isRunning {
		sockets, err := poller.Poll(time.Second)
		if err != nil {
			cl.loggerFile.Write([]byte(fmt.Sprintln("Eroare la poll ", err)))
			break
		}

		for _, socket := range sockets {
			s := socket.Socket
			msg, _ := s.RecvBytes(0)

			switch s {
			case cl.SocketInputGenerator:
				cl.SocketServer.Send(msg, padding)
				cl.loggerFile.Write([]byte(fmt.Sprintf("Sending to port %s\n", cl.ServerAddress)))
			}
		}
	}
}

func (cl *Client) receiveImagesAndAudio() {
	var imageByte, audioByte = byte('0'), byte('1')

	for cl.isRunning {
		message, err := cl.SocketServer.Receive(padding)
		if err != nil {
			cl.loggerFile.Write([]byte(fmt.Sprintln("Error receiving image or sound ", err)))
			break
		}

		switch message[0] {
		case imageByte:
			cl.SocketImageDisplayer.Send(string(message[1:]), zmq.DONTWAIT)
		case audioByte:
			cl.SocketSoundPlayer.Send(string(message[1:]), zmq.DONTWAIT)
		}
	}
}

func (cl *Client) Stop() {
	cl.isRunning = false

	for _, process := range cl.Processes {
		process.Signal(syscall.SIGINT)
		cl.loggerFile.Write([]byte(fmt.Sprintf("Inchis %d\n", process.Pid)))
	}

	cl.SocketInputGenerator.Close()
	cl.SocketImageDisplayer.Close()
	cl.SocketSoundPlayer.Close()

	if cl.SocketServer != (communication.TCPConnection{}) {
		cl.SocketServer.Close()
	}
}

func main() {
	file, _ := os.Create("/home/robert/Desktop/clientLog.txt")

	if len(os.Args) != 3 {
		file.Write([]byte("Imi trebuie 2 paramteri\n"))
		os.Exit(1)
	}

	cl, err := NewClient(os.Args[1], os.Args[2], file)
	if err != nil {
		file.Write([]byte(fmt.Sprintf("Clientul nu s-a activat %s", err)))
	}

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		file.Write([]byte(fmt.Sprintln("Client oprit")))
		cl.Stop()
	}()

	cl.Start()
}
