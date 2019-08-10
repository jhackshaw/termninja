#!/bin/bash
host="play.term.ninja"
port=3333
token=""
unencrypted=false
realtime=false
anonymous=false
debug_output=false


if [ "$1" = "--help" ]
then
  echo
  echo "termninja:  client scripts to connect to a termninja host"
  echo "\t-h HOST\t\ttermninja host to connect to (default play.term.ninja)"
  echo "\t-p PORT\t\ttermninja port to connect to (default 3333)"
  echo "\t-t TOKEN\tplay token to connect with (default anonymous)"
  echo "\t-g GAME\t\tindex of game to start automatically"
  echo "\t-a\t\tplay anonymously"
  echo "\t-i\t\twhether to play 'interactively' (e.g. snake game)"
  echo "\t-u\t\tuse an unencrypted connection (for development)"
  echo "\t-d\t\tdebug command - only show the command that will run don't execute\n"
  exit 0;
fi
  


while getopts ":h:p:t:g:auid" opt; do
  case "$opt" in
    h)
      host=${OPTARG}
      ;;
    p)
      port=${OPTARG}
      ;;
    t)
      token=${OPTARG}
      ;;
    g)
      game=${OPTARG}
      ;;
    a)
      anonymous=true
      ;;
    u)
      unencrypted=true
      ;;
    i)
      realtime=true
      ;;
    d)
      debug_output=true
      ;;
    :)
      echo "Invalid option: $OPTARG requires an argument" 1>&2
      ;;
  esac
done


command=""
data=""

# add stty -icanon if necessary
if [ ${realtime} = true ]
then
  command="stty -icanon && "
fi

# send token if it exists
if [ -n "$token" ] || [ $anonymous = true ]
then
  # token=${<~/.termninja/token.txt}
  data="$token\n\n"
fi


# autostart game at gameindex if specified
if [ -n "$game" ]
then
  data="$data$game\n"
  echo -e "\n"
fi

if [ -n "$data" ]
then
  command="$command (echo -e '$data' && cat ) | "
fi

if [ $unencrypted = true ]
then
  command="$command ncat $host $port"
else
  command="$command openssl s_client -async -quiet -connect $host:$port 2>/dev/null"
fi


if [ $debug_output = true ]
then
  echo $command
else
  eval $command
fi
