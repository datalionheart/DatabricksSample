namespace SimQueue
{
    public partial class FuncSendMessage2EventHub
    {
        public class SendProperty
        {
            public string Sender { get; set; }
            public string Content { get; set; }
            public string SendDatetime { get; set; }
            public string CountryCode { get; set; }
            public int RandomValue { get; set; }
        }
    }
}
