// Initialize config server replica set
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "configsvr:27019" }]
});

// Initialize shard1
rs.initiate({
  _id: "shard1ReplSet",
  members: [{ _id: 0, host: "shard1:27018" }]
});

// Initialize shard2
rs.initiate({
  _id: "shard2ReplSet",
  members: [{ _id: 0, host: "shard2:27018" }]
});

// Configure mongos
sh.addShard("shard1ReplSet/shard1:27018");
sh.addShard("shard2ReplSet/shard2:27018");

// Enable sharding for our database and collection
sh.enableSharding("tracker");
sh.shardCollection("tracker.products", { url: "hashed" });