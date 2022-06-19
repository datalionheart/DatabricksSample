using System;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;
using System.Text;
using Newtonsoft.Json;

namespace SimQueue
{
    public partial class FuncSendMessage2EventHub
    {
        [FunctionName("FuncSendMessage2EventHub")]
        public void Run([TimerTrigger("*/5 * * * * *")] TimerInfo myTimer, ILogger log)
        {
            _ = SendMessage2EventHub();
        }

        private const string strCountry = "ABW,AFG,AGO,AIA,ALA,ALB,AND,ARE,ARG,ARM,ASM,ATA,ATF,ATG,AUS,AUT,AZE,BDI,BEL,BEN,BES,BFA,BGD,BGR,BHR,BHS,BIH,BLM,BLR,BLZ,BMU,BOL,BRA,BRB,BRN,BTN,BVT,BWA,CAF,CAN,CCK,CHE,CHL,CHN,CIV,CMR,COD,COG,COK,COL,COM,CPV,CRI,CUB,CUW,CXR,CYM,CYP,CZE,DEU,DJI,DMA,DNK,DOM,DZA,ECU,EGY,ERI,ESH,ESP,EST,ETH,FIN,FJI,FLK,FRA,FRO,FSM,GAB,GBR,GEO,GGY,GHA,GIB,GIN,GLP,GMB,GNB,GNQ,GRC,GRD,GRL,GTM,GUF,GUM,GUY,HKG,HMD,HND,HRV,HTI,HUN,IDN,IMN,IND,IOT,IRL,IRN,IRQ,ISL,ISR,ITA,JAM,JEY,JOR,JPN,KAZ,KEN,KGZ,KHM,KIR,KNA,KOR,KWT,LAO,LBN,LBR,LBY,LCA,LIE,LKA,LSO,LTU,LUX,LVA,MAC,MAF,MAR,MCO,MDA,MDG,MDV,MEX,MHL,MKD,MLI,MLT,MMR,MNE,MNG,MNP,MOZ,MRT,MSR,MTQ,MUS,MWI,MYS,MYT,NAM,NCL,NER,NFK,NGA,NIC,NIU,NLD,NOR,NPL,NRU,NZL,OMN,PAK,PAN,PCN,PER,PHL,PLW,PNG,POL,PRI,PRK,PRT,PRY,PSE,PYF,QAT,REU,ROU,RUS,RWA,SAU,SDN,SEN,SGP,SGS,SHN,SJM,SLB,SLE,SLV,SMR,SOM,SPM,SRB,SSD,STP,SUR,SVK,SVN,SWE,SWZ,SXM,SYC,SYR,TCA,TCD,TGO,THA,TJK,TKL,TKM,TLS,TON,TTO,TUN,TUR,TUV,TWN,TZA,UGA,UKR,UMI,URY,USA,UZB,VAT,VCT,VEN,VGB,VIR,VNM,VUT,WLF,WSM,YEM,ZAF,ZMB,ZWE";
        private const string connectionString = "Endpoint=sb://ehdebezcdc.servicebus.windows.net/;SharedAccessKeyName=Producer;SharedAccessKey=KhHrkfxGbvQ7i1HX3YnLChhr/WxrBe1o2jZcGmkpX78=";
        private const string eventHubName = "datasim";
        private static EventHubProducerClient producerClient;

        private static async Task SendMessage2EventHub()
        {
            // Create a producer client that you can use to send events to an event hub
            producerClient = new EventHubProducerClient(connectionString, eventHubName);

            // Create a batch of events 
            using EventDataBatch eventBatch = await producerClient.CreateBatchAsync();

            SendProperty SendMessage = new SendProperty();
            SendMessage.Sender = $"Sender{new Random().Next(10, 100)}";
            SendMessage.Content = Guid.NewGuid().ToString();
            SendMessage.SendDatetime = DateTime.Now.ToString("O");
            SendMessage.CountryCode = strCountry.Split(',')[new Random().Next(0, strCountry.Split(',').Length)];
            SendMessage.RandomValue = new Random().Next(0, 1000);

            var json = JsonConvert.SerializeObject(SendMessage);

            if (!eventBatch.TryAdd(new EventData(Encoding.UTF8.GetBytes(json.ToString()))))
            {
                // if it is too large for the batch
                throw new Exception($"ERROR: {json} cannot be sent.");
            }

            try
            {
                // Use the producer client to send the batch of events to the event hub
                await producerClient.SendAsync(eventBatch);
                Console.WriteLine($"INFO: {json} has been published.");
            }
            finally
            {
                await producerClient.DisposeAsync();
            }
        }
    }
}
