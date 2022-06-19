package pathlib

import (
	"fmt"
	"os"
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

func GetCurrentPath() Path {
	currentPath, _ := os.Getwd()
	return Path{Name: currentPath}
}
