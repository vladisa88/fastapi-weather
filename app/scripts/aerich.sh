#!/usr/bin/env bash

aerich init-db && aerich migrate && aerich upgrade && python main.py
