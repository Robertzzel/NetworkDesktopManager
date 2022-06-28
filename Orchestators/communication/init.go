package communication

import (
	"io"
	"net"
	"strconv"
)

type TCPConnection struct {
	net.Conn
}

func padNumber(number int, padding int) string {
	numberString := strconv.Itoa(number)
	for len(numberString) < padding {
		numberString = "0" + numberString
	}
	return numberString
}

func (conn TCPConnection) Send(message []byte, sizePadding int) {
	conn.Write([]byte(padNumber(len(message), sizePadding)))
	conn.Write(message)
}

func (conn TCPConnection) Receive(sizePadding int) ([]byte, error) {

	sizeBytes, err := io.ReadAll(io.LimitReader(conn, int64(sizePadding)))
	if err != nil {
		return nil, err
	}

	size, err := strconv.Atoi(string(sizeBytes))
	if err != nil {
		return nil, err
	}

	msg, err := io.ReadAll(io.LimitReader(conn, int64(size)))
	if err != nil {
		return nil, err
	}

	return msg, nil
}
