'use strict';
module.exports = (sequelize, DataTypes) => {
  const HeartRate = sequelize.define('HeartRate', {
    sumFFTs: {type: DataTypes.DOUBLE, allowNull:true},
    correlatedPk_Pk: {type: DataTypes.DOUBLE, allowNull:true},
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