#!/bin/bash
sysctl -w wm.max_map_count=262144
sudo sysctl -p
