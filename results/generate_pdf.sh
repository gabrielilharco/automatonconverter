#!/bin/bash

inp=$1

dot -Tpdf $inp.dot -o $inp.pdf 