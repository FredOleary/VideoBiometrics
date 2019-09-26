var express = require('express');

const db = require('../models/index');
const Device = db.sequelize.models.Device;
var router = express.Router();

router.post('/', function(req, res, next) {
  return Device.findOrCreate({
    where: {
      device:      req.body.device,
    },
    defaults:{
      description:  req.body.description,
      name:  req.body.name
    }
  })
  .then( (result) => {
    const [newDevice, wasCreated] = result;
    if( newDevice.description == req.body.description &&
        newDevice.name == req.body.name ){
      res.send(newDevice);
    }else{
      newDevice.update({
        description: req.body.description,
        name: req.body.name
      })
      .then((newDevice) => {
        res.send(newDevice);
      })
      Device.update
    }
  }).catch( err =>{
    next(err);
  })
});

module.exports = router;
