
HOST_PORT=$1
shift

HOST=$(echo "$HOST_PORT" | cut -d: -f1)
PORT=$(echo "$HOST_PORT" | cut -d: -f2)

echo "Waiting for $HOST:$PORT..."

while ! nc -z $HOST $PORT; do
    sleep 1
done
echo "$HOST:$PORT is up now"
exec "$@"
