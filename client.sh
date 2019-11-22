#!/bin/bash

host="play.term.ninja"
# endpoint="https://play.term.ninja"
port=3333
token=""

login=false
logout=false
register=false
unencrypted=false
realtime=false
anonymous=false
debug_output=false

# command to execute (dynamically generated)
command=""

# data to send (token and game choice if specified)
data=""

if [ "$1" = "--help" ]
then
  echo
  echo -e "termninja:  client scripts to connect to a termninja host\n"
  echo -e "\t-h HOST\t\ttermninja host to connect to (default play.term.ninja)"
  echo -e "\t-p PORT\t\ttermninja port to connect to (default 3333)"
  echo -e "\t-g GAME\t\tindex of game to start automatically"
  # echo -e "\t-e ENDPOINT\thttp(s) endpoint to log in to with -l"
  echo -e "\t-l\t\tlogin to termninja server using https api at endpoint provided by -e"
  echo -e "\t-L\t\tLogout"
  echo -e "\t-r\t\tRegister"
  echo -e "\t-a\t\tplay anonymously"
  echo -e "\t-i\t\twhether to play 'interactively' (e.g. snake game)"
  echo -e "\t-u\t\tuse an unencrypted connection (for development)"
  echo -e "\t-d\t\tdebug command - only show the command that will run don't execute\n"
  exit 0;
fi


while getopts ":h:p:t:g:e:auidlr" opt; do
  case "$opt" in
    h)
      host=${OPTARG}
      ;;
    p)
      port=${OPTARG}
      ;;
    g)
      game=${OPTARG}
      ;;
    # e)
    #   endpoint=${OPTARG}
    #   ;;
    l)
      login=true
      ;;
    L)
      logout=true
      ;;
    r)
      register=true
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


# This endpoint is used for api calls
if [ ${unencrypted} = false ]
then
  endpoint="http://$host"
else
  endpoint="https://$host"
fi


# Register with the api
if [ ${register} = true ]
then
  echo -n "username: "
  read -r username
  echo -n "password: "
  read -r -s password
  echo -e -n "\nconfirm: "
  read -r -s confirm
  echo

  if [[ "$password" != "$confirm" ]]
  then
    echo "Passwords did not match"
    exit
  fi


  status_code=$(
    curl -d "username=$username"\
         -d "password=$password"\
         --write-out "%{http_code}\n"\
         -X POST "$endpoint/user"\
         -o /dev/null\
         -s
  )

  if [[ "$status_code" -ne 201 ]]
  then
    echo "Registration failed. Username may be taken."
  else
    echo "Registration successful. Login with -l"
  fi

  exit
fi


# Get a token from the api and save it in the user's home dir
# do nothing else if logging in
if [ ${login} = true ]
then
  mkdir -p ~/.termninja/

  echo -n "username: "
  read -r username
  echo -n "password: "
  read -r -s password
  echo

  status_code=$(
    curl -d "username=$username"\
        -d "password=$password"\
        --write-out "%{http_code}\n"\
        -X POST "$endpoint/user/retrieve_play_token"\
        -o ~/.termninja/token.txt\
        -s
  )

  echo "$status_code"

  if [[ "$status_code" -ne 200 ]]
  then
    echo "Login Failed"
    rm -f ~/.termninja/token.txt
  else
    echo "Login Succeeded"
  fi;

  exit
fi


# Delete the saved token effectively logging the user out
if [ ${logout} = true ]
then 
  rm -f ~/.termninja/token.txt
  echo "Logged out"
  exit
fi



# add stty -icanon if necessary
if [ ${realtime} = true ]
then
  command="stty -icanon && "
fi

# send token if it exists
if [ -e ~/.termninja/token.txt ]
then
  token=$(<~/.termninja/token.txt)
  data="$token\n\n"
fi

# sent empty line if playing anonymously
if [ $anonymous = true ]
then
  data="\n\n"
fi

# autostart game at gameindex if specified
if [ -n "$game" ]
then
  data="$data$game\n"
fi

# pipe any initial data to stdin if appropriate
if [ -n "$data" ]
then
  command="$command (echo -e '$data' && cat ) | "
fi

# unencrypted = netcat
# encrypted = openssl s_client
if [ $unencrypted = true ]
then
  command="$command ncat $host $port"
else
  command="$command openssl s_client -async -quiet -verify 3 -verify_return_error --tls1_2 -connect $host:$port 2>/dev/null"
fi


if [ $debug_output = true ]
then
  echo $command
else
  eval $command
fi
