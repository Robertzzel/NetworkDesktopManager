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

var EnvInterpretorPath = pathlib.GetCurrentPath().GetParent().Add("venv").Add("bin").Add("python3")

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

func NewServer(clientImageAddress string, clientAudioAddress string, clientInputAddress string) ApplicationServer {
	context, _ := zmq.NewContext()
	SocketImageClient, _ := context.NewSocket(zmq.PUSH)
	SocketAudioClient, _ := context.NewSocket(zmq.PUSH)
	SocketInputClient, _ := context.NewSocket(zmq.PULL)
	SocketImageGenerator, _ := context.NewSocket(zmq.PULL)
	SocketSoundGenerator, _ := context.NewSocket(zmq.PULL)
	SocketInputExecutor, _ := context.NewSocket(zmq.PUSH)

	SocketImageClient.Bind(fmt.Sprintf("tcp://%s", clientImageAddress))
	SocketAudioClient.Bind(fmt.Sprintf("tcp://%s", clientAudioAddress))
	SocketInputClient.Bind(fmt.Sprintf("tcp://%s", clientInputAddress))
	SocketImageGenerator.Bind("tcp://*:5111")
	SocketSoundGenerator.Bind("tcp://*:5222")
	SocketInputExecutor.Bind("tcp://*:5333")

	return ApplicationServer{
		SocketImageClient:    SocketImageClient,
		SocketAudioClient:    SocketAudioClient,
		SocketInputClient:    SocketInputClient,
		SocketImageGenerator: SocketImageGenerator,
		SocketSoundGenerator: SocketSoundGenerator,
		SocketInputExecutor:  SocketInputExecutor,
		isRunning:            false,
	}
}

func startPythonProcess(argv []string) *os.Process {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)
	cmd.Start()
	return cmd.Process
}

func (sv *ApplicationServer) Start() {
	basePath := pathlib.GetCurrentPath().GetParent()
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

	fmt.Print(os.Getpid())
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
	sv := NewServer("*:5001", "*:5002", "*:5003")

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		fmt.Println("Se intrerupe")
		sv.Stop()
	}()

	sv.Start()
}
