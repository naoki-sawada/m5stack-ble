const noble = require('noble');

const DEVICE_NAME = 'm5-stack';
const SERVICE_UUID = '4fafc2011fb5459e8fccc5c9c331914b';
const CHARACTERISTIC_UUID = 'beb5483e36e14688b7f5ea07361b26a8';

noble.on('stateChange', state => {
  if (state === 'poweredOn') {
    console.log('Scanning');
    noble.startScanning();
  } else {
    noble.stopScanning();
  }
});

noble.on('discover', peripheral => {
  const { localName } = peripheral.advertisement;
  if (localName === DEVICE_NAME) {
    noble.stopScanning();
    console.log(`Connecting to '${localName}' ${peripheral.id}`);
    connectAndSetUp(peripheral);
  }
});

function connectAndSetUp(peripheral) {
  peripheral.connect(error => {
    console.log('Connected to', peripheral.id);

    // specify the services and characteristics to discover
    const serviceUUIDs = [SERVICE_UUID];
    const characteristicUUIDs = [CHARACTERISTIC_UUID];

    peripheral.discoverSomeServicesAndCharacteristics(
      serviceUUIDs,
      characteristicUUIDs,
      onServicesAndCharacteristicsDiscovered,
    );
  });
  
  peripheral.on('disconnect', () => console.log('disconnected'));
}

function onServicesAndCharacteristicsDiscovered(error, services, characteristics) {
  console.log('Discovered services and characteristics');
  const characteristic = characteristics[0];

  characteristic.subscribe();
  characteristic.on('data', (data) => {
    console.log('Received: ', data.toString('utf8'));
  });

  characteristic.read((error, data) => {
    console.log('Read: ', data.toString('utf8'));
  });

  const message = new Buffer('hello, ble', 'utf-8');
  console.log("Sending:  '" + message + "'");
  characteristic.write(message);
}

