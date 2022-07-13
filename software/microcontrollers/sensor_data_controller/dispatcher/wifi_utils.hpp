/**
 * Function to connect dispatcher to wifi network
 *
 * @param {String} ssid wifi network id
 * @param {String} password
 */
void connectWifi(String ssid, String password)
{
  Serial.println("setting up wifi...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(), password.c_str());

  // in case you want static ip
  // WiFi.config(ip, gateway, subnet);
  int i = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(200);
    Serial.print(++i);
    Serial.print(' ');
  }

  Serial.println("");
  Serial.print("Connected to (STA):\t");
  Serial.println(WiFi.SSID());
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
}