package main

import (
	"errors"
	"fmt"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"syscall"

	"example.com/orchestrators/communication"
	"example.com/orchestrators/pathlib"

	zmq "github.com/pebbe/zmq4"
)

var EnvInterpretorPath = pathlib.GetCurrentPath().GetParent().GetParent().GetParent().Add("venv").Add("bin").Add("python3")

const padding = 10

type ApplicationServer struct {
	listeningAddress     *net.TCPAddr
	listener             *net.TCPListener
	loggerFile           *os.File
	socketImageGenerator *zmq.Socket
	socketSoundGenerator *zmq.Socket
	socketInputExecutor  *zmq.Socket
	processes            []*os.Process
	clientConnection     communication.TCPConnection
	isRunning            bool
}

func NewServer(address string, loggerFile *os.File) (ApplicationServer, error) {
	context, _ := zmq.NewContext()
	socketImageGenerator, _ := context.NewSocket(zmq.PULL)
	socketSoundGenerator, _ := context.NewSocket(zmq.PULL)
	socketInputExecutor, _ := context.NewSocket(zmq.PUSH)

	listeningAddress, err := net.ResolveTCPAddr("tcp", address)
	if err != nil {
		return ApplicationServer{}, err
	}

	return ApplicationServer{
		listener:             nil,
		clientConnection:     communication.TCPConnection{},
		listeningAddress:     listeningAddress,
		loggerFile:           loggerFile,
		socketImageGenerator: socketImageGenerator,
		socketSoundGenerator: socketSoundGenerator,
		socketInputExecutor:  socketInputExecutor,
		isRunning:            false,
	}, nil
}

func (sv *ApplicationServer) Start() error {
	defer sv.Stop()
	sv.isRunning = true

	if err := sv.socketImageGenerator.Bind("tcp://*:5111"); err != nil {
		return err
	}
	if err := sv.socketSoundGenerator.Bind("tcp://*:5222"); err != nil {
		return err
	}
	if err := sv.socketInputExecutor.Bind("tcp://*:5333"); err != nil {
		return err
	}

	var err error
	sv.listener, err = net.ListenTCP("tcp", sv.listeningAddress)
	if err != nil {
		sv.log(fmt.Sprintf("Error while listening %s\n", err))
		return err
	}
	sv.log(fmt.Sprintf("Listening to %s:%d...\n", sv.listeningAddress.IP, sv.listeningAddress.Port))

	conn, err := sv.listener.Accept()
	if err != nil {
		sv.log("Server oprit din ascultat\n")
		return err
	}
	sv.clientConnection = communication.TCPConnection{Conn: conn}
	sv.log("Client connected...\n")

	sv.log("Opening processes...\n")
	if err := sv.startProcesses(); err != nil {
		sv.log(fmt.Sprintln(err))
		return err
	}

	sv.log("Routing messages...\n")
	if err := sv.routeMessages(); err != nil {
		return err
	}

	return nil
}

func (sv *ApplicationServer) startProcesses() error {
	basePath := pathlib.GetCurrentPath().GetParent().GetParent().GetParent()
	imageGeneratorPath := basePath.Add("Producers").Add("image_generator.py")
	soundGeneratorPath := basePath.Add("Producers").Add("sound_generator.py")
	inputExecutorPath := basePath.Add("Consumers").Add("input_executor.py")

	if !EnvInterpretorPath.FileExists() {
		return errors.New("enviroment path does not exist")
	}
	if !imageGeneratorPath.FileExists() || !soundGeneratorPath.FileExists() || !inputExecutorPath.FileExists() {
		return errors.New("processes cannot be open, one of the file does not exists")
	}

	imageGeneratorProcess, err := startPythonProcess([]string{imageGeneratorPath.ToString(), "5111"})
	if err != nil {
		return err
	}
	audioGeneratorProcess, err := startPythonProcess([]string{soundGeneratorPath.ToString(), "5222"})
	if err != nil {
		return err
	}
	inputExecutorProcess, err := startPythonProcess([]string{inputExecutorPath.ToString(), "5333"})
	if err != nil {
		return err
	}

	sv.processes = append(sv.processes, imageGeneratorProcess, audioGeneratorProcess, inputExecutorProcess)

	return nil
}

func startPythonProcess(argv []string) (*os.Process, error) {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)

	if err := cmd.Start(); err != nil {
		return nil, err
	}
	return cmd.Process, nil
}

func (sv *ApplicationServer) routeMessages() error {
	//errorClientInputs := make(chan error)
	//go sv.handleReceivingMessages(errorClientInputs)

	if err := sv.handleSendingMessages(); err != nil {
		return err
	}

	return nil //<-errorClientInputs
}

func (sv *ApplicationServer) handleReceivingMessages(output chan error) {
	for sv.isRunning {
		command, err := sv.clientConnection.Receive(padding)
		if err != nil {
			sv.log(fmt.Sprintln("client inchis, nu mai pot primi comenzi ", err))
			output <- err
			return
		}

		sv.socketInputExecutor.Send(string(command), zmq.DONTWAIT)
	}
	output <- nil
}

func (sv *ApplicationServer) handleSendingMessages() error {
	poller := zmq.NewPoller()
	poller.Add(sv.socketImageGenerator, zmq.POLLIN)
	poller.Add(sv.socketSoundGenerator, zmq.POLLIN)

	for sv.isRunning {
		sockets, err := poller.Poll(-1)
		if err != nil {
			sv.log(fmt.Sprintln("Poller oprit, ", err))
			return err
		}

		for _, socket := range sockets {
			s := socket.Socket
			msg, _ := s.RecvBytes(0)

			switch s {
			case sv.socketImageGenerator:
				msg := append([]byte("0"), msg...)
				sv.clientConnection.Send(msg, padding)

			case sv.socketSoundGenerator:
				msg := append([]byte("1"), msg...)
				sv.clientConnection.Send(msg, padding)
			}
		}
	}
	return nil
}

func (sv *ApplicationServer) Stop() {
	sv.isRunning = false

	sv.log("Closing processes...\n")
	for _, process := range sv.processes {
		if err := process.Signal(syscall.SIGINT); err != nil {
			sv.log(fmt.Sprintf("Procesul %d nu a putut fi inchis\n", process.Pid))
		} else {
			sv.log(fmt.Sprintf("Inchis %d\n", process.Pid))
		}
	}

	sv.log("Closing ZMQ sockets...\n")
	sv.socketImageGenerator.Close()
	sv.socketSoundGenerator.Close()
	sv.socketInputExecutor.Close()

	sv.log("CLosing listener and client conn...\n")
	if sv.clientConnection != (communication.TCPConnection{}) {
		sv.clientConnection.Close()
	}
	if sv.listener != nil {
		sv.listener.Close()
	}

	sv.log("Server closed...\n")
}

func (sv *ApplicationServer) log(msg string) {
	sv.loggerFile.Write([]byte(msg))
}

func main() {
	file, _ := os.Create("/home/robert/Desktop/serverlog.txt")

	if len(os.Args) != 2 {
		file.Write([]byte(fmt.Sprintln("Nu am destui parametri")))
		os.Exit(1)
	}

	sv, err := NewServer(os.Args[1], file)
	if err != nil {
		file.Write([]byte(fmt.Sprintf("Eroate la creare server %s\n", err)))
		os.Exit(1)
	}

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		file.Write([]byte("Stopping...\n"))
		sv.Stop()
	}()

	if err := sv.Start(); err != nil {
		file.Write([]byte(fmt.Sprintf("Eroate la rularea serverului %s\n", err)))
	}
}
