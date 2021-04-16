#!/bin/bash

# 传入容器名称
containerName=$1
currTime=`date +"%Y-%m-%d %H:%M:%S"`

# 查看进程是否存在
exist=`docker inspect --format '{{.State.Running}}' ${containerName}`

if [ "${exist}" != "true" ]; then
		docker start ${containerName}

		# 记录
		echo "${currTime} 重启docker容器，容器名称：${containerName}" >> /mnt/xvde1/ms_ctynyd/scripts/wbwf_monitor.log
	
fi
