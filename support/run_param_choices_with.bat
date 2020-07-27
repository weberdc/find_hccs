@echo off

@echo Started: %date% %time% 1>&2

set G_FILE=%1

set EXTRACT=python %~dp0\..\extract_hccs.py -i %G_FILE% --dry-run

rem goto :threshold

set OPTS=-s FSA_V --theta
%EXTRACT% %OPTS% 0.1
set OPTS=--no-header -s FSA_V --theta
%EXTRACT% %OPTS% 0.2
%EXTRACT% %OPTS% 0.3
%EXTRACT% %OPTS% 0.4
%EXTRACT% %OPTS% 0.5
%EXTRACT% %OPTS% 0.6
%EXTRACT% %OPTS% 0.7
%EXTRACT% %OPTS% 0.8
%EXTRACT% %OPTS% 0.9

rem goto :end
:threshold

set OPTS=-s THRESHOLD --threshold
%EXTRACT% %OPTS% 0.1
set OPTS=--no-header -s THRESHOLD --threshold
%EXTRACT% %OPTS% 0.2
%EXTRACT% %OPTS% 0.3
%EXTRACT% %OPTS% 0.4
%EXTRACT% %OPTS% 0.5
%EXTRACT% %OPTS% 0.6
%EXTRACT% %OPTS% 0.7
%EXTRACT% %OPTS% 0.8
%EXTRACT% %OPTS% 0.9

:end
@echo Ended:   %date% %time% 1>&2

