#!/usr/bin/env bash

CONFIG=spder_supervisord.conf

start() {
	status
	if [ ! $? -eq 0 ]; then
		echo "process is already running.."
		return 1
	fi

    mkdir -p logs

	pip install --user supervisor -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

    # 启动后台程序
	supervisord -c ${CONFIG}

    echo "process start success..."
}

stop() {

    ps -ef | grep -v grep | grep  supervisord | grep -w ${CONFIG} | awk '{print $2}' | xargs kill -9

     # 先关闭监控脚本
    ret=`ps -ef | grep -v grep | grep -w lanuch_cp_spider.py | awk '{print $2}'`
    if [ -z "${ret}" ]; then
	    echo "lanuch_cp_spider.py not running.."
	else
	    kill -9 ${ret}
	fi

	echo "process stop success..." && return 1
}

restart() {
    stop
    sleep 1
    start
}

status() {

    result=1
    pid=`ps -ef | grep -v grep | grep  supervisord | grep -w ${CONFIG} | awk '{print $2}'`
    if [ -z "${pid}" ]; then
        echo "后台管理服务不存在..."
        result=0
    else
        echo "supervisord ${pid}"
    fi
    return ${result}
}

case "$1" in
	start|stop|restart|status)
  		$1
		;;
	*)
		echo $"Usage: $0 {start|stop|status|restart}"
		exit 1
esac
