var express = require('express');
const db = require('../models/index');
const HeartRate = db.sequelize.models.HeartRate;
var router = express.Router();


router.get('/', function(req, res, next) {
  return HeartRate.findAll({
    raw: true,
    where:{DeviceId:req.query.deviceId}
  }).then(function(result){
    res.send(result);
  }).catch( err =>{
    next(err);
  })
});
router.post('/', function(req, res, next) {
  return HeartRate.create({
    sumFFTs:req.body.sumFFTs,
    DeviceId:req.body.deviceId
  }).then( newHeartRate => {
    res.send(newHeartRate);
  }).catch( err =>{
    next(err);
  })
});

module.exports = router;
