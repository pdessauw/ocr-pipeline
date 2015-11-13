#!/bin/bash
nosetests packages/pipeline packages/apputils packages/denoiser --cover-package=apputils --cover-package=denoiser --cover-package=pipeline
