var express = require('express');
// var batchData = require('../utilities/batchData');

const db = require('../models/index');
const Device = db.sequelize.models.Device;
var router = express.Router();


router.get('/', function(req, res, next) {
  return Device.findAll({
    raw: true
  }).then(function(result){
    res.send(result);
  }).catch( err =>{
    next(err);
  })
});

// router.post('/', function(req, res, next) {
//   // let device = {};

//   // device.name = req.body.name;
//   // if( req.body.hasOwnProperty("description"))
//   //   device.description = req.body.description;
//   // else
//   //   device.description = "N/A"

//   return Device.findOrCreate({
//     where: {
//       device:      req.body.device,
//     },
//     defaults:{
//       description:  req.body.description,
//       name:  req.body.name
//     }
//   })
//   .then( (result) => {
//     const [newDevice, wasCreated] = result;
//     if( newDevice.description == req.body.description &&
//         newDevice.name == req.body.name ){
//       res.send(newDevice);
//     }else{
//       newDevice.update({
//         description: req.body.description,
//         name: req.body.name
//       })
//       .then((newDevice) => {
//         res.send(newDevice);
//       })
//       Device.update
//     }
//   }).catch( err =>{
//     next(err);
//   })
// });

module.exports = router;
