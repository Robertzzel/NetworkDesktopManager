package pathlib

import (
	"errors"
	"fmt"
	"os"
	"runtime"
	"strings"
)

type Path struct {
	Name string
}

func (p Path) GetParent() Path {
	parent := strings.Split(p.Name, "/")
	p.Name = strings.Join(parent[:len(parent)-1], "/")
	return p
}

func (p Path) Add(name string) Path {
	p.Name = fmt.Sprintf("%s/%s", p.Name, name)
	return p
}

func (p Path) ToString() string {
	return p.Name
}

func (p Path) FileExists() bool {
	if _, err := os.Stat(p.Name); errors.Is(err, os.ErrNotExist) {
		return false
	}
	return true
}

func GetCurrentPath() Path {
	_, fileName, _, _ := runtime.Caller(1)
	return Path{Name: fileName}
}
