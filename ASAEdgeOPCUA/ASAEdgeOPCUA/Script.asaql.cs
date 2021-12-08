using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;


namespace ASAEdgeOPCUA
{
    public class Class1
    {
        public static Dictionary<String, object> GetValue(Dictionary<String, object> payload){

            Dictionary<string, object> result = new Dictionary<string, object>();
            Dictionary<string, object> val = (Dictionary<string, object>) payload.Values.ElementAt(0);
            String nodeId = payload.Keys.ElementAt(0);

             if ((string)val["Value"] == "uninitialized")
             {
                result.Add("status", "uninitialized");
                result.Add("uri", nodeId);
                return result;
             }
             else if (nodeId.Contains("i=2013"))
             {
                  using (Stream stream = GenertateStream((string)val["Value"]))
                  {
                    var serializer = new DataContractJsonSerializer(typeof(payloadi2013));
                    payloadi2013 parsedPayload = (payloadi2013)serializer.ReadObject(stream);

                    result.Add("NodeId", "ns=1;i=2013");
                    if (parsedPayload.version == null) { result.Add("versioin", "null"); }
                    else { result.Add("version", parsedPayload.version); }
                    if (parsedPayload.safemode == null) { result.Add("safemode", "null"); }
                    else { result.Add("safemode", parsedPayload.safemode); }
                    result.Add("status", "parsed");
                  }
                return result;
            }
            else
            {
                result.Add("status", "node could no be parsed");
                return result;
            }    
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

        public static Stream GenertateStream(string s)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(s);
            writer.Flush();
            stream.Position = 0;
            return stream;
        }
    }

    [DataContract]
    class payloadi2013
    {
        [DataMember(Name = "safemode")] public string safemode { get; set; }
        [DataMember(Name = "version")] public string version { get; set; }

    }
}
