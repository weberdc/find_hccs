@echo off

rem apply decaying sliding window treatment to 15m, 60m, 360m and 1440m graphs
rem using alpha = 0.5, 0.7 and 0.9

@echo Started: %date% %time% 1>&2

rem parameterise this
set BEHAVIOUR=retweets
set NUM_WINDOWS=5

rem if not exist "%BEHAVIOUR%" mkdir %BEHAVIOUR%
if not exist "%BEHAVIOUR%\15m-0.5"   mkdir %BEHAVIOUR%\15m-0.5
if not exist "%BEHAVIOUR%\15m-0.7"   mkdir %BEHAVIOUR%\15m-0.7
if not exist "%BEHAVIOUR%\15m-0.9"   mkdir %BEHAVIOUR%\15m-0.9
if not exist "%BEHAVIOUR%\60m-0.5"   mkdir %BEHAVIOUR%\60m-0.5
if not exist "%BEHAVIOUR%\60m-0.7"   mkdir %BEHAVIOUR%\60m-0.7
if not exist "%BEHAVIOUR%\60m-0.9"   mkdir %BEHAVIOUR%\60m-0.9
if not exist "%BEHAVIOUR%\360m-0.5"  mkdir %BEHAVIOUR%\360m-0.5
if not exist "%BEHAVIOUR%\360m-0.7"  mkdir %BEHAVIOUR%\360m-0.7
if not exist "%BEHAVIOUR%\360m-0.9"  mkdir %BEHAVIOUR%\360m-0.9
if not exist "%BEHAVIOUR%\1440m-0.5" mkdir %BEHAVIOUR%\1440m-0.5
if not exist "%BEHAVIOUR%\1440m-0.7" mkdir %BEHAVIOUR%\1440m-0.7
if not exist "%BEHAVIOUR%\1440m-0.9" mkdir %BEHAVIOUR%\1440m-0.9

set APPLY_WINDOW=python %LCN_BIN%\apply_decaying_sliding_window.py

set OPTS=-p weight -w %NUM_WINDOWS%


set ALPHA=0.5
set WINDOW=15m
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.7
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.9
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%

set ALPHA=0.5
set WINDOW=60m
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.7
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.9
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%

set ALPHA=0.5
set WINDOW=360m
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.7
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.9
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%

set ALPHA=0.5
set WINDOW=1440m
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.7
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%
set ALPHA=0.9
echo %WINDOW%-%ALPHA%: %date% %time% 1>&2
%APPLY_WINDOW% -i %BEHAVIOUR%\%WINDOW% -o %BEHAVIOUR%\%WINDOW%-%ALPHA% -a %ALPHA% %OPTS%


@echo Ended:   %date% %time% 1>&2
