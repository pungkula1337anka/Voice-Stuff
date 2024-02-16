
<h1 align="center">
<br>

Voice Butler

</h1><br>
<br><br>

HA Voice assistant ESP code.

<br><br><br>


- **1: Flash ESP with ESPHome** <br>

Put in battery, done.





<br><br>





## 🦆 /esphome/ESP32-S3-BOX3.yaml <br>


<br>


```
substitutions:
  
  name: roboduck-assistant
  friendly_name: RoboDuck Assistant
  
  loading_illustration_file: !secret butler_pic
  idle_illustration_file: !secret butler_pic
  listening_illustration_file: !secret butler_pic
  thinking_illustration_file: !secret butler_pic
  replying_illustration_file: !secret butler_pic
  error_illustration_file: !secret butler_pic

  loading_illustration_background_color: "FFFF00"
  idle_illustration_background_color: "000000"
  listening_illustration_background_color: "0000FF"
  thinking_illustration_background_color: "FFFF00"
  replying_illustration_background_color: "00FF00"
  error_illustration_background_color: "FF0000"

  voice_assist_idle_phase_id: "1"
  voice_assist_listening_phase_id: "2"
  voice_assist_thinking_phase_id: "3"
  voice_assist_replying_phase_id: "4"
  voice_assist_not_ready_phase_id: "10"
  voice_assist_error_phase_id: "11"
  voice_assist_muted_phase_id: "12"

esphome:
  name: butler
  friendly_name: butler
  name_add_mac_suffix: false
  platformio_options:
    board_build.flash_mode: dio
  project:
    name: esphome.voice-assistant
    version: "1.0"
  min_version: 2023.11.5
  on_boot:
    priority: 600
    then:
      - script.execute: draw_display
      - delay: 30s
      - if:
          condition:
            lambda: return id(init_in_progress);
          then:
            - lambda: id(init_in_progress) = false;
            - script.execute: draw_display


esp32:
  board: esp32-s3-devkitc-1
  flash_size: 16MB
  framework:
    type: esp-idf
    sdkconfig_options:
      CONFIG_ESP32S3_DEFAULT_CPU_FREQ_240: "y"
      CONFIG_ESP32S3_DATA_CACHE_64KB: "y"
      CONFIG_ESP32S3_DATA_CACHE_LINE_64B: "y"
      CONFIG_AUDIO_BOARD_CUSTOM: "y"
      CONFIG_ESP32_S3_BOX_3_BOARD: "y"
    components:
      - name: esp32_s3_box_3_board
        source: github://jesserockz/esp32-s3-box-3-board@main
        refresh: 0s

psram:
  mode: octal
  speed: 80MHz

external_components:
  - source: github://pr#5230
    components: esp_adf
    refresh: 0s

api:
  encryption:
    key: !secret api_key
#Custom Creates a service to start listening
  services:
    - service: va_start
      then:
        - voice_assistant.start:
            silence_detection: true     
           
    - service: va_stop
      then:
        - voice_assistant.stop


  #  - service: va_wake_word_on
  #    then:
  #      - lambda: id(va).set_use_wake_word(true);    
  #         
  #  - service: va_wake_word_off
  #    then:
  #      - lambda: id(va).set_use_wake_word(false);



  on_client_connected:
    - script.execute: draw_display
  on_client_disconnected:
    - script.execute: draw_display

logger:
  hardware_uart: USB_SERIAL_JTAG

dashboard_import:
  package_import_url: github://esphome/firmware/voice-assistant/esp32-s3-box-3.yaml@main


ota:
  password: !secret api_key

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  ap:
  on_connect:
    - script.execute: draw_display
    - delay: 5s # Gives time for improv results to be transmitted
    - ble.disable:
  on_disconnect:
    - script.execute: draw_display
    - ble.enable:

improv_serial:

esp32_improv:
  authorizer: none

#i2c:
#  - id: bus_a
#    sda: GPIO08
#    scl: GPIO18
#    scan: true
#
#  - sda: GPIO41
#    scl: GPIO40
#    id: bus_b

########
sensor:
########  
#  - platform: aht10
#    i2c_id: bus_b
#    variant: AHT20
#    temperature:
#      name: "Temperature"
#    humidity:
#      name: "Humidity"
#    update_interval: 45s

  - platform: adc
    pin: GPIO10
    name: "Battery voltage"
    id: battery_voltage
    unit_of_measurement: "V"
    accuracy_decimals: 3
    device_class: "voltage"
    entity_category: "diagnostic"
    update_interval: 30s
    filters:
        - multiply: 4.01

  - platform: copy
    source_id: battery_voltage
    name: "Battery level"
    unit_of_measurement: "%"
    accuracy_decimals: 1
    device_class: "battery"
    entity_category: "diagnostic"
    filters:
      - lambda: return (x - 2.5) / (4.2 - 2.5) * 100;
      - clamp:
          min_value: 0
          max_value: 100
          ignore_out_of_range: true

time:
  - platform: homeassistant
    id: time_ha
    timezone: Europe/Stockholm

#remote_receiver:
#  pin: GPIO38
#  dump: all
  # Settings to optimize recognition of RF devices
  #tolerance: 50%
  #filter: 250us
  #idle: 4ms
  #buffer_size: 2kb

#remote_transmitter:
 # pin: GPIO39
 # carrier_duty_percent: 100%



button:
  - platform: restart
    name: "Reboot Butler"
    entity_category: "diagnostic"

  - platform: shutdown
    name: "Stäng av Butler"
    entity_category: "diagnostic"



  - platform: factory_reset
    id: factory_reset_btn
    name: NOLLSTÄLL Butler

number:
  - platform: template
    name: "Presence duration"
    id: radar_delayed_off
    icon: mdi:account-clock
    optimistic: true
    restore_value: true
    initial_value: 60
    min_value: 0
    step: 5
    max_value: 300
    unit_of_measurement: s
    entity_category: config
    mode: box

binary_sensor:
  - platform: gpio
    pin:
      number: GPIO21
    name: "Presence detect"
    disabled_by_default: false
    device_class: "occupancy"
    filters:
      - delayed_off: !lambda return id(radar_delayed_off).state * 1000;
    on_release:
      then:
        - if:
            condition: 
              switch.is_on: mute_when_absent
            then:
              - switch.turn_on: mute
              - light.turn_off: led
    on_press:
      then:
        - if:
            condition: 
              switch.is_on: mute_when_absent
            then:
              - switch.turn_off: mute
              - light.turn_on: led
  - platform: gpio
    pin:
      number: GPIO1
      inverted: true
    name: "Mute"
    disabled_by_default: true
    entity_category: diagnostic

  - platform: gpio
    pin:
      number: GPIO0
      mode: INPUT_PULLUP
      inverted: true
    name: Top Left Button
    disabled_by_default: true
    entity_category: diagnostic
    #on_click:
    #    then:
    #        - button.press: restart_btn
    on_multi_click:
      - timing:
          - ON for at least 10s
        then:
          - button.press: factory_reset_btn

output:
  - platform: ledc
    pin: GPIO47
    id: backlight_output

light:
  - platform: monochromatic
    id: led
    name: LCD Backlight
    entity_category: config
    output: backlight_output
    restore_mode: RESTORE_DEFAULT_ON
    default_transition_length: 250ms

esp_adf:
  board: esp32s3box3

#i2s_audio:
#  - i2s_lrclk_pin: GPIO45
#    i2s_bclk_pin: GPIO17
#media_player:
#  - platform: i2s_audio
#    name: None
#    id: mediaplayer
#    dac_type: external
#    i2s_dout_pin: GPIO16
#    mode: mono
#    mute_pin:
#      number: GPIO1
#      inverted: True

microphone:
  - platform: esp_adf
    id: box_mic
########
speaker:
  - platform: esp_adf
    id: box_speaker
########

voice_assistant:
  id: va
  microphone: box_mic
  speaker: box_speaker
  #media_player:
  use_wake_word: true
  noise_suppression_level: 0
  auto_gain: 31dBFS
  volume_multiplier: 2.0
  vad_threshold: 3
  on_listening:
    - lambda: id(voice_assistant_phase) = ${voice_assist_listening_phase_id};
    - script.execute: draw_display
  #on_wake_word_detected:
   # - homeassistant.service:
   #     service: media_player.play_media
   #     data:
   #       entity_id: media_player.ha 
   #       media_content_id: https://pungkula.duckdns.org:1337/local/sound/qwack.mp3
   #       media_content_type: music
  #        announce: "true"   
  on_stt_vad_end:
    - lambda: id(voice_assistant_phase) = ${voice_assist_thinking_phase_id};
    - script.execute: draw_display
  #on_stt_end: 
  on_tts_stream_start:
    - lambda: id(voice_assistant_phase) = ${voice_assist_replying_phase_id};
    - script.execute: draw_display
      
  on_tts_stream_end:
    - lambda: id(voice_assistant_phase) = ${voice_assist_idle_phase_id};
    - script.execute: draw_display
 
 #SEND TTS TO MEDIA PLAYER
  #on_tts_start:
  #   - delay: 1s
  #   - homeassistant.service:
 #       service: tts.speak
  #      data:
  #        media_player_entity_id: media_player.ha
  #        message: !lambda 'return x;'
  on_tts_end:
    - delay: 5s
    - homeassistant.service:
        service: media_player.play_media
        data:
          entity_id: media_player.ha
          media_content_id: !lambda 'return x;'
          media_content_type: music
          announce: "true"   
  on_error:
    - if:
        condition:
          lambda: return !id(init_in_progress);
        then:
          - lambda: id(voice_assistant_phase) = ${voice_assist_error_phase_id};
          - script.execute: draw_display
          - delay: 1s
          - if:
              condition:
                switch.is_off: mute
              then:
                - lambda: id(voice_assistant_phase) = ${voice_assist_idle_phase_id};
              else:
                - lambda: id(voice_assistant_phase) = ${voice_assist_muted_phase_id};
          - script.execute: draw_display
  on_client_connected:
    - if:
        condition:
          switch.is_off: mute
        then:
          - wait_until:
              not: ble.enabled
          - voice_assistant.start_continuous:
          - lambda: id(voice_assistant_phase) = ${voice_assist_idle_phase_id};
        else:
          - lambda: id(voice_assistant_phase) = ${voice_assist_muted_phase_id};
    - lambda: id(init_in_progress) = false;
    - script.execute: draw_display
  on_client_disconnected:
    - lambda: id(voice_assistant_phase) = ${voice_assist_not_ready_phase_id};
    - script.execute: draw_display

script:
  - id: draw_display
    then:
      - if:
          condition:
            lambda: return !id(init_in_progress);
          then:
            - if:
                condition:
                  wifi.connected:
                then:
                  - if:
                      condition:
                        api.connected:
                      then:
                        - lambda: |
                            switch(id(voice_assistant_phase)) {
                              case ${voice_assist_listening_phase_id}:
                                id(s3_box_lcd).show_page(listening_page);
                                id(s3_box_lcd).update();
                                break;
                              case ${voice_assist_thinking_phase_id}:
                                id(s3_box_lcd).show_page(thinking_page);
                                id(s3_box_lcd).update();
                                break;
                              case ${voice_assist_replying_phase_id}:
                                id(s3_box_lcd).show_page(replying_page);
                                id(s3_box_lcd).update();
                                break;
                              case ${voice_assist_error_phase_id}:
                                id(s3_box_lcd).show_page(error_page);
                                id(s3_box_lcd).update();
                                break;
                              case ${voice_assist_muted_phase_id}:
                                id(s3_box_lcd).show_page(muted_page);
                                id(s3_box_lcd).update();
                                break;
                              case ${voice_assist_not_ready_phase_id}:
                                id(s3_box_lcd).show_page(no_ha_page);
                                id(s3_box_lcd).update();
                                break;
                              default:
                                id(s3_box_lcd).show_page(idle_page);
                                id(s3_box_lcd).update();
                            }
                      else:
                        - display.page.show: no_ha_page
                        - component.update: s3_box_lcd
                else:
                  - display.page.show: no_wifi_page
                  - component.update: s3_box_lcd
          else:
            - display.page.show: initializing_page
            - component.update: s3_box_lcd

switch:
  - platform: template
    name: "Mute when absent"
    id: mute_when_absent
    icon: mdi:account-right-arrow
    optimistic: true
    entity_category: config
    restore_mode: RESTORE_DEFAULT_OFF
  - platform: template
    name: Mute
    id: mute
    optimistic: true
    restore_mode: RESTORE_DEFAULT_OFF
    entity_category: config
    on_turn_off:
      - if:
          condition:
            lambda: return !id(init_in_progress);
          then:
            - lambda: id(va).set_use_wake_word(true);
            - lambda: id(voice_assistant_phase) = ${voice_assist_idle_phase_id};
            - if:
                condition:
                  not:
                    - voice_assistant.is_running
                then:
                  - voice_assistant.start_continuous
            - script.execute: draw_display
    on_turn_on:
      - if:
          condition:
            lambda: return !id(init_in_progress);
          then:
            - voice_assistant.stop
            - lambda: id(va).set_use_wake_word(false);
            - lambda: id(voice_assistant_phase) = ${voice_assist_muted_phase_id};
            - script.execute: draw_display
 # - platform: template
 #   name: Assist
 #   id: assistera
 #   optimistic: true
 #   restore_mode: RESTORE_DEFAULT_OFF
 #   entity_category: config
 #   on_turn_on:
 #     - if:
 #         condition: voice_assistant.is_running
 #         then:
 #           - voice_assistant.stop
 #         else:
 #           - voice_assistant.start_continuous
 #   on_turn_off:
 #     - then:
 #           - voice_assistant.stop

  - platform: template
    name: Use wake word
    id: use_wake_word
    optimistic: true
    restore_mode: RESTORE_DEFAULT_OFF
    entity_category: config
    on_turn_on:
      - lambda: id(va).set_use_wake_word(true);
      - if:
          condition:
            not:
              - voice_assistant.is_running
          then:
            - voice_assistant.start_continuous
    on_turn_off:
      - voice_assistant.stop
      - lambda: id(va).set_use_wake_word(false);

globals:
  - id: init_in_progress
    type: bool
    restore_value: no
    initial_value: "true"
  - id: voice_assistant_phase
    type: int
    restore_value: no
    initial_value: ${voice_assist_not_ready_phase_id}

image:
  - file: ${error_illustration_file}
    id: casita_error
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: ${idle_illustration_file}
    id: casita_idle
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: ${listening_illustration_file}
    id: casita_listening
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: ${thinking_illustration_file}
    id: casita_thinking
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: ${replying_illustration_file}
    id: casita_replying
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: ${loading_illustration_file}
    id: casita_initializing
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: https://github.com/esphome/firmware/raw/main/voice-assistant/error_box_illustrations/error-no-wifi.png
    id: error_no_wifi
    resize: 320x240
    type: RGB24
    use_transparency: true
  - file: https://github.com/esphome/firmware/raw/main/voice-assistant/error_box_illustrations/error-no-ha.png
    id: error_no_ha
    resize: 320x240
    type: RGB24
    use_transparency: true

color:
  - id: idle_color
    hex: ${idle_illustration_background_color}
  - id: listening_color
    hex: ${listening_illustration_background_color}
  - id: thinking_color
    hex: ${thinking_illustration_background_color}
  - id: replying_color
    hex: ${replying_illustration_background_color}
  - id: loading_color
    hex: ${loading_illustration_background_color}
  - id: error_color
    hex: ${error_illustration_background_color}

spi:
  clk_pin: 7
  mosi_pin: 6

display:
  - platform: ili9xxx
    id: s3_box_lcd
    model: S3BOX
    data_rate: 40MHz
    cs_pin: 5
    dc_pin: 4
    reset_pin:
      number: 48
      inverted: true
    update_interval: never
    pages:
      - id: idle_page
        lambda: |-
          it.fill(id(idle_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_idle), ImageAlign::CENTER);
      - id: listening_page
        lambda: |-
          it.fill(id(listening_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_listening), ImageAlign::CENTER);
      - id: thinking_page
        lambda: |-
          it.fill(id(thinking_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_thinking), ImageAlign::CENTER);
      - id: replying_page
        lambda: |-
          it.fill(id(replying_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_replying), ImageAlign::CENTER);
      - id: error_page
        lambda: |-
          it.fill(id(error_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_error), ImageAlign::CENTER);
      - id: no_ha_page
        lambda: |-
          it.image((it.get_width() / 2), (it.get_height() / 2), id(error_no_ha), ImageAlign::CENTER);
      - id: no_wifi_page
        lambda: |-
          it.image((it.get_width() / 2), (it.get_height() / 2), id(error_no_wifi), ImageAlign::CENTER);
      - id: initializing_page
        lambda: |-
          it.fill(id(loading_color));
          it.image((it.get_width() / 2), (it.get_height() / 2), id(casita_initializing), ImageAlign::CENTER);
      - id: muted_page
        lambda: |-
          it.fill(Color::BLACK);

```

<br><br>
