/*
© | 2026
main.go

Entry point for the sentinel CLI
*/

package main

import (
	"sentinel/internal/cli"
	_ "sentinel/internal/scanner"
)

func main() {
	cli.Execute()
}
