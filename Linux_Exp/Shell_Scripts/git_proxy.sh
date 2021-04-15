#!/bin/bash
case $1 in
 
on)
git config --global http.https://github.com.proxy 'http://127.0.0.1:8889' 
git config --global https.https://github.com.proxy 'http://127.0.0.1:8889'
;;
 
off)
git config --global --unset http.https://github.com.proxy
git config --global --unset https.https://github.com.proxy
;;
 
status)
git config --get http.https://github.com.proxy
git config --get https.https://github.com.proxy
;;
esac
exit 0
