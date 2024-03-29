var express = require('express');
// var batchData = require('../utilities/batchData');

const db = require('../models/index');
const Device = db.sequelize.models.Device;
const HeartRate = db.sequelize.models.HeartRate;
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

router.delete('/', function(req, res, next) {
  if( req.query.deviceId == -1 ){
    return Device.destroy({
      where: {},
      truncate: false
    }).then(function(result){
      res.send(200);
    }).catch( err =>{
      next(err);
    })
  }else{
    return Device.destroy({
      where:{id:req.query.deviceId}
    }).then(function(result){
      res.send(200);
    }).catch( err =>{
      next(err);
    })
  }
});
module.exports = router;
