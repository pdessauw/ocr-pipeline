#!/bin/bash
nosetests -v packages/pipeline packages/apputils packages/denoiser --with-coverage --cover-erase --cover-package=apputils --cover-package=denoiser --cover-package=pipeline
