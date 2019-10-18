'use strict';
module.exports = (sequelize, DataTypes) => {
  const Device = sequelize.define('Device', {
    device: {type: DataTypes.STRING, allowNull: false},
    name: {type: DataTypes.STRING, allowNull: false},
    video: {type: DataTypes.STRING, allowNull: false},
    description: {type: DataTypes.STRING, allowNull: true}

  }, {});
  Device.associate = function(models) {
    Device.hasMany(models.HeartRate);
  };
  return Device;
};