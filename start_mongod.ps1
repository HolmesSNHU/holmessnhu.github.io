Start-Process mongod.exe -ArgumentList '--config', '.\database\mongod.conf' -Verb RunAs
Read-Host -Prompt "Press Enter to exit"