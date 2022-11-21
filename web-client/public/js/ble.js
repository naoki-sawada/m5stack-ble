async function onButtonClick() {
  let serviceUuid = "4fafc201-1fb5-459e-8fcc-c5c9c331914b";
  let characteristicUuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8";
  let device = null;

  try {
    console.log('Requesting Bluetooth Device...');
    device = await navigator.bluetooth.requestDevice({
      filters: [
        { services: [serviceUuid] },
        { name: ["m5-stack"] },
      ],
    });
  
    console.log('Connecting to GATT Server...');
    const server = await device.gatt.connect();

    console.log('Getting Service...');
    const service = await server.getPrimaryService(serviceUuid);

    console.log('Getting Characteristics...');
    const characteristics = await service.getCharacteristics(characteristicUuid);

    if (characteristics.length > 0) {
      const myCharacteristic = characteristics[0];

      console.log('Reading Characteristics...');
      const value = await myCharacteristic.readValue();
      const decoder = new TextDecoder('utf-8');
      console.log(decoder.decode(value));

      const encoder = new TextEncoder('utf-8');
      const text = 'hi!'; 
      await myCharacteristic.writeValue(encoder.encode(text));

      await myCharacteristic.startNotifications();
      myCharacteristic.addEventListener('characteristicvaluechanged', (event) => {
        const value = event.target.value;
        const decoder = new TextDecoder('utf-8');
        console.log(decoder.decode(value));
      });

      console.log('Waiting 60 seconds to receive data from the device...')
      await sleep(60 * 1000);
    }
  } finally {
    if (device) {
      if (device.gatt.connected) {
        device.gatt.disconnect();
        console.log('disconnect');
      }
    }
  }
  
  if (device) {
    if (device.gatt.connected) {
      device.gatt.disconnect();
      console.log('disconnect');
    }
  }
}

async function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}
