#!/bin/bash
sysctl -w vm.max_map_count=262144
sudo sysctl -p 
