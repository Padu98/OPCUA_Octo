using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;


namespace ASAEdgeOPCUA
{
    public class Class1
    {
        public static Dictionary<String, object> []GetValue(Dictionary<String, object> payload)
        {
            Dictionary<string, object>[] array = new Dictionary<string, object>[payload.Values.Count];  //result array

            for (int i = 0; i < payload.Values.Count; i++)
            {
                Dictionary<string, object> result = new Dictionary<string, object>();
                Dictionary<string, object> val = (Dictionary<string, object>)payload.Values.ElementAt(i); //davor 0
                result.Add("TimeStamp", (string)val["SourceTimestamp"]);

                Dictionary<string, object> restResult = new Dictionary<string, object>(); 
                String nodeId = payload.Keys.ElementAt(i);

                if ((string)val["Value"] == "empty")
                {
                    restResult.Add("status", "empty");
                    restResult.Add("NodeId", nodeId);
                    result.Add("restResult", restResult);
                         
                }
                else if (nodeId.Contains("i=2013"))
                {
                    using (Stream stream = GenerateStream((string)val["Value"]))
                    {
                        var serializer = new DataContractJsonSerializer(typeof(payloadi2013));
                        payloadi2013 parsedPayload = (payloadi2013)serializer.ReadObject(stream);

                        restResult.Add("ns=1;i=2013", "Server information");
                        if (parsedPayload.version == null) { restResult.Add("server version", "null"); }
                        else { restResult.Add("server version", parsedPayload.version); }
                        if (parsedPayload.safemode == null) { restResult.Add("safemode", "null"); }
                        else { restResult.Add("safemode", parsedPayload.safemode); }
                        restResult.Add("status", "parsed");
                    }
                    result.Add("restResult", restResult);
                }
                else if (nodeId.Contains("i=2012"))
                {
                    using (Stream stream = GenerateStream((string)val["Value"]))
                    {
                        var serializer = new DataContractJsonSerializer(typeof(payloadi2012));
                        payloadi2012 parsedPayload = (payloadi2012)serializer.ReadObject(stream);

                        restResult.Add("ns=1;i=2012", "Version information");
                        if (parsedPayload.api == null) { restResult.Add("api", "null"); }
                        else { restResult.Add("api", parsedPayload.api); }
                        if (parsedPayload.server == null) { restResult.Add("server", "null"); }
                        else { restResult.Add("server", parsedPayload.server); }
                        if (parsedPayload.text == null) { restResult.Add("text", "null"); }
                        else { restResult.Add("text", parsedPayload.text); }
                        restResult.Add("status", "parsed");
                    }
                    result.Add("restResult", restResult); ;


                }/*
           else if (nodeId.Contains("i=2017"))
            {
                string json = (string)val["Value"];
                List<string> keyvalues = findValueList(json, "name");
                restResult.Add("ns=1;i=2017", "File Information");

                for (int i = 0; i < keyvalues.Count; i++)
                {
                    restResult.Add("File_" + (i+1).ToString(), keyvalues.ElementAt(i));
                }
                restResult.Add("status", "parsed");
                result.Add("restResult", restResult);
            }
            else if (nodeId.Contains("i=2025"))
            {
                using (Stream stream = GenertateStream((string)val["Value"]))
                {
                    var serializer = new DataContractJsonSerializer(typeof(payloadi2025));
                    payloadi2025 parsedPayload = (payloadi2025)serializer.ReadObject(stream);

                    Dictionary<string, object> flags = new Dictionary<string, object>();
                    flags.Add("operational", parsedPayload.flags.operational);
                    flags.Add("paused", parsedPayload.flags.paused);
                    flags.Add("printing", parsedPayload.flags.printing);
                    flags.Add("cancelling", parsedPayload.flags.cancelling);
                    flags.Add("pausing", parsedPayload.flags.pausing);
                    flags.Add("sdReady", parsedPayload.flags.sdReady);
                    flags.Add("error", parsedPayload.flags.error);
                    flags.Add("ready", parsedPayload.flags.ready);
                    flags.Add("closedOrError", parsedPayload.flags.closedOrError);

                    restResult.Add("ns=1;i=2012", "Version information");
                    restResult.Add("flags", flags);
                    restResult.Add("status", "parsed");
                }
                result.Add("restResult", restResult);
            }
            else if (nodeId.Contains("i=232132123"))
            {
                string json = (string)val["Value"];
                string tool = "tool";
             
                List<string> actualList = findValueList(json, "actual");
                List<string> targetList = findValueList(json, "target");
                List<string> offsetList = findValueList(json, "offset");

                Dictionary<string, object> tools;
                for (int i = 0; i < actualList.Count -1; i++)
                {
                    tools = new Dictionary<string, object>();
                    tools.Add("actual", actualList.ElementAt(i));
                    tools.Add("target", targetList.ElementAt(i));
                    tools.Add("offset", offsetList.ElementAt(i));
                    restResult.Add(tool + i.ToString(), tools);
                }

                tools = new Dictionary<string, object>();
                tools.Add("actual", actualList.ElementAt(actualList.Count-1));
                tools.Add("target", targetList.ElementAt(actualList.Count-1));
                tools.Add("offset", offsetList.ElementAt(actualList.Count-1));
                restResult.Add("bed", json.ToString());

               result.Add("restResult", restResult);
            }*/
                else
                {
                    result.Add("status", "node could no be parsed");
                   // return result;
                }
                array[i] = result;
            }
            return array;
        }

        public static string GetTimeStamp(Dictionary<string, object> payload)
        {
            Dictionary<string, object> val = (Dictionary<string, object>)payload.Values.ElementAt(0);
            if (val.ContainsKey("SourceTimestamp"))
            {
                return (string)val["SourceTimestamp"];
            }
            return "no timestamp found";
        }

        public static Stream GenerateStream(string s)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(s);
            writer.Flush();
            stream.Position = 0;
            return stream;
        }

        /*  public static List<String> findValueList(string json, string key)
          {
              StringBuilder sb = new StringBuilder("", 50);
              int position = 1;

              List<String> result = new List<String>();
              string cleanjson = json.Trim(new Char[] { '"', '\'' });

              while (position > 0)
              {
                  position = cleanjson.LastIndexOf(key + ":") + 1;
                  if (position > 0)
                  {
                      char nextChar = cleanjson[position];
                      while (nextChar != ',' && nextChar != '}')
                      {
                          sb.Append(nextChar);
                          position += 1;
                          nextChar = cleanjson[position];
                      }
                      result.Add(sb.ToString());
                      cleanjson.Remove(position - 1); //change key
                      sb = new StringBuilder("", 50);
                  }
              }
              return result;
          }*/
    }

    [DataContract]
    class payloadi2013 //server information
    {
        [DataMember(Name = "safemode")] public string safemode { get; set; }
        [DataMember(Name = "version")] public string version { get; set; }

    }

    [DataContract]
    class payloadi2012 //version information
    {
        [DataMember(Name = "api")] public string api { get; set; }
        [DataMember(Name = "server")] public string server { get; set; }
        [DataMember(Name = "text")] public string text { get; set; }

    }

    [DataContract]
    class payloadi2025 //printer state (ohne temperature)
    {
        [DataMember(Name = "text")] public string text { get; set; }
        [DataMember(Name = "flags")] public flags flags { get; set; }

    }

    [DataContract]
    class flags 
    {
        [DataMember(Name = "operational")] public bool operational { get; set; }
        [DataMember(Name = "paused")] public bool paused { get; set; }
        [DataMember(Name = "printing")] public bool printing { get; set; }
        [DataMember(Name = "cancelling")] public bool cancelling { get; set; }
        [DataMember(Name = "pausing")] public bool pausing { get; set; }
        [DataMember(Name = "sdReady")] public bool sdReady { get; set; }
        [DataMember(Name = "error")] public bool error { get; set; }
        [DataMember(Name = "ready")] public bool ready { get; set; }
        [DataMember(Name = "closedOrError")] public bool closedOrError { get; set; }

    }
}

