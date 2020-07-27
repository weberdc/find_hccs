@echo off

rem combine the 15m, 60m, 360m and 1440m LCNs, including
rem alpha = 0.5, 0.7 and 0.9

@echo Started: %date% %time% 1>&2

rem parameterise this
set BEHAVIOUR=retweets
set CORPUS=sapol

set COMBINE_LCNS=python %LCN_BIN%\combine_lcns.py

rem set OPTS=-v
set OPTS=


set WINDOW=15m
set KEY=%WINDOW%
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%

set WINDOW=60m
set KEY=%WINDOW%
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%

set WINDOW=360m
set KEY=%WINDOW%
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%

set WINDOW=1440m
set KEY=%WINDOW%
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.5
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.7
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%
set KEY=%WINDOW%-0.9
echo %KEY%: %date% %time% 1>&2
%COMBINE_LCNS% -i %BEHAVIOUR%\%KEY% -o %BEHAVIOUR%\%CORPUS%-%BEHAVIOUR%-%KEY%-combined.graphml %OPTS%


@echo Ended:   %date% %time% 1>&2
