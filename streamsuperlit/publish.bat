@REM set TWINE_REPOSITORY 4choob-pip-server
@REM set TWINE_REPOSITORY_URL http://192.168.1.5:83
@REM twine upload --repository-url http://192.168.1.5:83 dist/*

scp ./dist/*.whl root@192.168.1.5:/storage/pip-server/
ssh root@192.168.1.5 "cd ~/local-services; docker-compose restart pip-server"