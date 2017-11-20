var redis = require('redis');
var client = redis.createClient(6379,'127.0.0.1');
var client_intoKEY = redis.createClient(6379,'127.0.0.1',{'db':1});

client.subscribe('test');

client.on('message',function(channel,data){
  var ob = eval("("+data+")");
  if(ob.acctno != undefined && ob.time != undefined && ob.acctno != '' && ob.time != '')
             {
    acctno = ob.acctno
    time = ob.time
    str = time + '@' + acctno
    client_intoKEY.lpush(acctno,str)
    client_intoKEY.zincrby('acctnoList',1,acctno)
	     }
 })
