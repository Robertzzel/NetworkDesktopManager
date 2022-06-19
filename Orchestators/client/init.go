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

var EnvInterpretorPath = pathlib.GetCurrentPath().GetParent().GetParent().GetParent().Add("venv").Add("bin").Add("python3")

type Client struct {
	SocketImageServer    *zmq.Socket
	SocketAudioServer    *zmq.Socket
	SocketInputServer    *zmq.Socket
	SocketImageDisplayer *zmq.Socket
	SocketSoundPlayer    *zmq.Socket
	SocketInputGenerator *zmq.Socket
	Processes            []*os.Process
	isRunning            bool
}

func startPythonProcess(argv []string) *os.Process {
	cmd := exec.Command(EnvInterpretorPath.ToString(), argv...)
	cmd.Start()
	return cmd.Process
}

func NewClient(imageAddress string, audioAddress string, inputAddress string, imageDisplayerAddress string) Client {
	context, _ := zmq.NewContext()
	socketImageServer, _ := context.NewSocket(zmq.PULL)
	socketAudioServer, _ := context.NewSocket(zmq.PULL)
	socketInputServer, _ := context.NewSocket(zmq.PUSH)
	socketImageDisplayer, _ := context.NewSocket(zmq.PAIR)
	socketSoundPlayer, _ := context.NewSocket(zmq.PUSH)
	socketInputGenerator, _ := context.NewSocket(zmq.PULL)

	socketImageServer.Connect(fmt.Sprintf("tcp://%s", imageAddress))
	fmt.Printf("client connected to %s", imageAddress)
	socketAudioServer.Connect(fmt.Sprintf("tcp://%s", audioAddress))
	socketInputServer.Connect(fmt.Sprintf("tcp://%s", inputAddress))
	socketImageDisplayer.Connect(fmt.Sprintf("tcp://%s", imageDisplayerAddress))
	socketSoundPlayer.Bind("tcp://*:6111")
	socketInputGenerator.Bind("tcp://*:6222")

	return Client{
		SocketImageServer:    socketImageServer,
		SocketAudioServer:    socketAudioServer,
		SocketInputServer:    socketInputServer,
		SocketImageDisplayer: socketImageDisplayer,
		SocketSoundPlayer:    socketSoundPlayer,
		SocketInputGenerator: socketInputGenerator,
		isRunning:            false,
	}
}

func (cl *Client) Start() {
	basePath := pathlib.GetCurrentPath().GetParent().GetParent().GetParent()
	soundPlayerPath := basePath.Add("Consumers").Add("sound_player.py").ToString()
	inputGeneratorPath := basePath.Add("Producers").Add("input_generator.py").ToString()

	cl.Processes = append(cl.Processes, startPythonProcess([]string{soundPlayerPath, "6111"}))
	cl.Processes = append(cl.Processes, startPythonProcess([]string{inputGeneratorPath, "6222"}))

	cl.isRunning = true
	cl.routeMessages()
}

func (cl *Client) routeMessages() {
	poller := zmq.NewPoller()
	poller.Add(cl.SocketImageServer, zmq.POLLIN)
	poller.Add(cl.SocketAudioServer, zmq.POLLIN)
	poller.Add(cl.SocketInputGenerator, zmq.POLLIN)

	for cl.isRunning {
		sockets, err := poller.Poll(time.Second)
		if err != nil {
			fmt.Print(err)
			break
		}

		for _, socket := range sockets {
			s := socket.Socket
			msg, _ := s.Recv(0)

			fmt.Printf("primt mesaj cu lungimea %d", len(msg))

			switch s {
			case cl.SocketImageServer:
				cl.SocketImageDisplayer.Send(msg, zmq.DONTWAIT)
			case cl.SocketAudioServer:
				cl.SocketSoundPlayer.Send(msg, zmq.DONTWAIT)
			case cl.SocketInputGenerator:
				cl.SocketInputServer.Send(msg, zmq.DONTWAIT)
			}
		}
	}
}

func (cl *Client) Stop() {
	cl.isRunning = false

	for _, process := range cl.Processes {
		process.Signal(syscall.SIGINT)
		fmt.Printf("Inchis %d", process.Pid)
	}

	cl.SocketImageServer.Close()
	cl.SocketAudioServer.Close()
	cl.SocketInputGenerator.Close()
	cl.SocketImageDisplayer.Close()
	cl.SocketSoundPlayer.Close()
	cl.SocketInputServer.Close()
}

func main() {
	if len(os.Args) != 5 {
		os.Exit(1)
	}

	cl := NewClient(os.Args[1], os.Args[2], os.Args[3], os.Args[4])

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT)
	go func() {
		<-sig
		fmt.Println("Clientul se intrerupe")
		cl.Stop()
	}()

	cl.Start()
}
