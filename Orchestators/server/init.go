package main

import (
	"fmt"
	"os"
	"os/exec"
	"os/signal"
	"syscall"
	"time"

	"example.com/orchestrators/pathlib"
	zmq "github.com/pebbe/zmq4"
)

var EnvInterpretorPath = pathlib.GetCurrentPath().GetParent().GetParent().Add("venv").Add("bin").Add("python3")

type ApplicationServer struct {
	SocketImageClient    *zmq.Socket
	SocketAudioClient    *zmq.Socket
	SocketInputClient    *zmq.Socket
	SocketImageGenerator *zmq.Socket
	SocketSoundGenerator *zmq.Socket
	SocketInputExecutor  *zmq.Socket
	Processes            []*os.Process
	isRunning            bool
}

func NewServer(imageAddress string, audioAddress string, inputAddress string) ApplicationServer {
	context, _ := zmq.NewContext()
	socketImageClient, _ := context.NewSocket(zmq.PUSH)
	socketAudioClient, _ := context.NewSocket(zmq.PUSH)
	socketInputClient, _ := context.NewSocket(zmq.PULL)
	socketImageGenerator, _ := context.NewSocket(zmq.PULL)
	socketSoundGenerator, _ := context.NewSocket(zmq.PULL)
	socketInputExecutor, _ := context.NewSocket(zmq.PUSH)

	socketImageClient.Bind(fmt.Sprintf("tcp://%s", imageAddress))
	socketAudioClient.Bind(fmt.Sprintf("tcp://%s", audioAddress))
	socketInputClient.Bind(fmt.Sprintf("tcp://%s", inputAddress))
	socketImageGenerator.Bind("tcp://*:5111")
	socketSoundGenerator.Bind("tcp://*:5222")
	socketInputExecutor.Bind("tcp://*:5333")

	return ApplicationServer{
		SocketImageClient:    socketImageClient,
		SocketAudioClient:    socketAudioClient,
		SocketInputClient:    socketInputClient,
		SocketImageGenerator: socketImageGenerator,
		SocketSoundGenerator: socketSoundGenerator,
		SocketInputExecutor:  socketInputExecutor,
		isRunning:            false,
	}
}

func startPythonProcess(argv []string) *os.Process {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)
	cmd.Start()
	return cmd.Process
}

func (sv *ApplicationServer) Start() {
	basePath := pathlib.GetCurrentPath().GetParent().GetParent()
	imageGeneratorPath := basePath.Add("Producers").Add("image_generator.py").ToString()
	soundGeneratorPath := basePath.Add("Producers").Add("sound_generator.py").ToString()
	inputExecutorPath := basePath.Add("Consumers").Add("input_executor.py").ToString()

	sv.Processes = append(sv.Processes, startPythonProcess([]string{imageGeneratorPath, "5111"}))
	sv.Processes = append(sv.Processes, startPythonProcess([]string{soundGeneratorPath, "5222"}))
	sv.Processes = append(sv.Processes, startPythonProcess([]string{inputExecutorPath, "5333"}))

	sv.isRunning = true
	sv.routeMessages()
}

func (sv *ApplicationServer) routeMessages() {
	poller := zmq.NewPoller()
	poller.Add(sv.SocketImageGenerator, zmq.POLLIN)
	poller.Add(sv.SocketSoundGenerator, zmq.POLLIN)
	poller.Add(sv.SocketInputClient, zmq.POLLIN)

	for sv.isRunning {
		sockets, err := poller.Poll(time.Second)
		if err != nil {
			fmt.Println(err)
			break
		}

		for _, socket := range sockets {
			s := socket.Socket
			msg, _ := s.Recv(0)

			switch s {
			case sv.SocketImageGenerator:
				sv.SocketImageClient.Send(msg, zmq.DONTWAIT)
			case sv.SocketSoundGenerator:
				sv.SocketAudioClient.Send(msg, zmq.DONTWAIT)
			case sv.SocketInputClient:
				sv.SocketInputExecutor.Send(msg, zmq.DONTWAIT)
			}
		}
	}
}

func (sv *ApplicationServer) Stop() {
	sv.isRunning = false
	for _, process := range sv.Processes {
		process.Signal(syscall.SIGINT)
		fmt.Printf("Inchis %d", process.Pid)
	}

	sv.SocketImageClient.Close()
	sv.SocketAudioClient.Close()
	sv.SocketInputClient.Close()
	sv.SocketImageGenerator.Close()
	sv.SocketSoundGenerator.Close()
	sv.SocketInputExecutor.Close()
}

func main() {
	if len(os.Args) != 4 {
		os.Exit(1)
	}

	sv := NewServer(os.Args[1], os.Args[2], os.Args[3])

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		fmt.Println("Se intrerupe")
		sv.Stop()
	}()

	sv.Start()
}
