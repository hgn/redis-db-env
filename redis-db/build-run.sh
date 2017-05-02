if [ ! -d redis-stable ]; then
	wget http://download.redis.io/redis-stable.tar.gz
	tar xvzf redis-stable.tar.gz
	cd redis-stable
	make
fi

cd redis-stable
./src/redis-server
