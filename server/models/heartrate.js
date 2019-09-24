'use strict';
module.exports = (sequelize, DataTypes) => {
  const HeartRate = sequelize.define('HeartRate', {
    VerticalPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    VerticalFFT: {type: DataTypes.DOUBLE, allowNull:true},
    GreenPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    GreenFFT: {type: DataTypes.DOUBLE, allowNull:true},
    sumFFTs: {type: DataTypes.DOUBLE, allowNull:true},
    correlatedPkPk: {type: DataTypes.DOUBLE, allowNull:true},
    correlatedFFTs: {type: DataTypes.DOUBLE, allowNull:true}
  }, {});
  HeartRate.associate = function(models) {
    HeartRate.belongsTo(models.Device, {
      onDelete: "CASCADE",
      foreignKey: {
        allowNull: false
      }
    });
  };
  return HeartRate;
};