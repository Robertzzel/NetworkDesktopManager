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
		loggerFile.Write([]byte(fmt.Sprintf("Error while getting the address %s\n", err)))
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

func (sv *ApplicationServer) Start() {
	sv.isRunning = true

	sv.socketImageGenerator.Bind("tcp://*:5111")
	sv.socketSoundGenerator.Bind("tcp://*:5222")
	sv.socketInputExecutor.Bind("tcp://*:5333")

	var err error
	sv.listener, err = net.ListenTCP("tcp", sv.listeningAddress)
	if err != nil {
		sv.loggerFile.Write([]byte(fmt.Sprintf("Error while listening %s\n", err)))
		sv.Stop()
		return
	}
	sv.loggerFile.Write([]byte(fmt.Sprintf("Listening to %s:%d...\n", sv.listeningAddress.IP, sv.listeningAddress.Port)))

	conn, err := sv.listener.Accept()
	if err != nil {
		sv.loggerFile.Write([]byte("Server oprit din ascultat\n"))
		sv.Stop()
		return
	}
	sv.loggerFile.Write([]byte("Client connected...\n"))

	sv.clientConnection = communication.TCPConnection{conn}

	sv.loggerFile.Write([]byte("Opening processes...\n"))
	if err := sv.startProcesses(); err != nil {
		sv.loggerFile.Write([]byte(fmt.Sprintln(err)))
		sv.Stop()
		return
	}

	sv.loggerFile.Write([]byte("Routing messages...\n"))
	sv.routeMessages()
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

	sv.processes = append(sv.processes, startPythonProcess([]string{imageGeneratorPath.ToString(), "5111"}))
	sv.processes = append(sv.processes, startPythonProcess([]string{soundGeneratorPath.ToString(), "5222"}))
	sv.processes = append(sv.processes, startPythonProcess([]string{inputExecutorPath.ToString(), "5333"}))

	return nil
}

func startPythonProcess(argv []string) *os.Process {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)
	cmd.Start()
	return cmd.Process
}

func (sv *ApplicationServer) routeMessages() {
	defer sv.Stop()
	go sv.handleClientInputs()

	poller := zmq.NewPoller()
	poller.Add(sv.socketImageGenerator, zmq.POLLIN)
	poller.Add(sv.socketSoundGenerator, zmq.POLLIN)

	for sv.isRunning {
		sockets, err := poller.Poll(-1)
		if err != nil {
			sv.loggerFile.Write([]byte(fmt.Sprintln("Poller gata ", err)))
			break
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
}

func (sv *ApplicationServer) handleClientInputs() {
	for sv.isRunning {
		sv.loggerFile.Write([]byte(fmt.Sprintf("astept read la %s\n", sv.clientConnection.LocalAddr())))
		command, err := sv.clientConnection.Receive(padding)
		if err != nil {
			sv.loggerFile.Write([]byte(fmt.Sprintln("client inchis, nu mai pot primi comenzi ", err)))
			break
		}
		sv.loggerFile.Write([]byte("inout read\n"))

		sv.socketInputExecutor.Send(string(command), zmq.DONTWAIT)
	}
}

func (sv *ApplicationServer) Stop() {
	sv.isRunning = false

	for _, process := range sv.processes {
		process.Signal(syscall.SIGINT)
		sv.loggerFile.Write([]byte(fmt.Sprintf("Inchis %d\n", process.Pid)))
	}

	sv.socketImageGenerator.Close()
	sv.socketSoundGenerator.Close()
	sv.socketInputExecutor.Close()

	if sv.clientConnection != (communication.TCPConnection{}) {
		sv.clientConnection.Close()
	}
	if sv.listener != nil {
		sv.listener.Close()
	}

	sv.loggerFile.Write([]byte("Server closed...\n"))
}

func main() {
	file, _ := os.Create("/home/robert/Desktop/serverlog.txt")

	if len(os.Args) != 2 {
		file.Write([]byte(fmt.Sprintln("Nu am destui parametri")))
		os.Exit(1)
	}

	sv, err := NewServer(os.Args[1], file)
	if err != nil {
		file.Write([]byte(fmt.Sprintf("Serverul nu s-a activat %s\n", err)))
		os.Exit(1)
	}

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		file.Write([]byte("Stopping...\n"))
		sv.Stop()
	}()

	sv.Start()
	file.Write([]byte("end\n"))
}
