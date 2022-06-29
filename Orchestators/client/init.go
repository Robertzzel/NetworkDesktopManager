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

func NewClient(serverAddress string, imageDisplayerAddress string, loggerFile *os.File) Client {
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
	}
}

func (cl *Client) Start() error {
	defer cl.Stop()
	if err := cl.SocketImageDisplayer.Connect(fmt.Sprintf("tcp://%s", cl.imageDisplayerAddress)); err != nil {
		return err
	}
	if err := cl.SocketSoundPlayer.Bind("tcp://*:6111"); err != nil {
		return err
	}
	if err := cl.SocketInputGenerator.Bind("tcp://*:6222"); err != nil {
		return err
	}

	cl.log("Connecting to server..\n")
	connection, err := net.Dial("tcp", cl.ServerAddress)
	if err != nil {
		cl.log(fmt.Sprintf("Cannot connect to server %s", err))
		return err
	}
	cl.SocketServer = communication.TCPConnection{Conn: connection}

	cl.isRunning = true
	if err := cl.startProcesses(); err != nil {
		cl.log(fmt.Sprintln(err))
		return err
	}
	if err := cl.routeMessages(); err != nil {
		return err
	}

	return nil
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

	audioPlayerProcess, err := startPythonProcess([]string{soundPlayerPath.ToString(), "6111"})
	if err != nil {
		return err
	}
	inputGeneratorProcess, err := startPythonProcess([]string{inputGeneratorPath.ToString(), "6222"})
	if err != nil {
		return err
	}

	cl.Processes = append(cl.Processes, audioPlayerProcess, inputGeneratorProcess)
	return nil
}

func startPythonProcess(argv []string) (*os.Process, error) {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)

	if err := cmd.Start(); err != nil {
		return nil, err
	}
	return cmd.Process, nil
}

func (cl *Client) routeMessages() error {
	errorOutputImagesAndAudio := make(chan error)
	go cl.receiveImagesAndAudio(errorOutputImagesAndAudio)

	poller := zmq.NewPoller()
	poller.Add(cl.SocketInputGenerator, zmq.POLLIN)

	for cl.isRunning {
		sockets, err := poller.Poll(time.Second)
		if err != nil {
			cl.log(fmt.Sprintln("Eroare la poll ", err))
			return err
		}

		for _, socket := range sockets {
			s := socket.Socket
			msg, _ := s.RecvBytes(0)

			switch s {
			case cl.SocketInputGenerator:
				cl.SocketServer.Send(msg, padding)
			}
		}
	}
	return <-errorOutputImagesAndAudio
}

func (cl *Client) receiveImagesAndAudio(output chan error) {
	var imageByte, audioByte = byte('0'), byte('1')
	buffer := make([]byte, 110_000)

	for cl.isRunning {
		n, err := cl.SocketServer.ReceiveBuffer(padding, buffer)
		if err != nil {
			cl.log(fmt.Sprintln("Error receiving image or sound ", err))
			output <- err
			return
		}

		switch buffer[0] {
		case imageByte:
			cl.SocketImageDisplayer.Send(string(buffer[1:n]), zmq.DONTWAIT)
		case audioByte:
			cl.SocketSoundPlayer.Send(string(buffer[1:n]), zmq.DONTWAIT)
		}
	}
	output <- nil
}

func (cl *Client) Stop() {
	cl.isRunning = false

	for _, process := range cl.Processes {

		if err := process.Signal(syscall.SIGINT); err != nil {
			cl.log(fmt.Sprintf("Procesul %d nu s-a putut inchide\n", process.Pid))
		} else {
			cl.log(fmt.Sprintf("Inchis %d\n", process.Pid))
		}
	}

	cl.SocketInputGenerator.Close()
	cl.SocketImageDisplayer.Close()
	cl.SocketSoundPlayer.Close()

	if cl.SocketServer != (communication.TCPConnection{}) {
		cl.SocketServer.Close()
	}
}

func (cl *Client) log(msg string) {
	cl.loggerFile.Write([]byte(msg))
}

func main() {
	file, _ := os.Create("/home/robert/Desktop/clientLog.txt")

	if len(os.Args) != 3 {
		file.Write([]byte("Imi trebuie 2 paramteri\n"))
		os.Exit(1)
	}

	cl := NewClient(os.Args[1], os.Args[2], file)

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		file.Write([]byte(fmt.Sprintln("Client oprit")))
		cl.Stop()
	}()

	if err := cl.Start(); err != nil {
		return
	}
}
