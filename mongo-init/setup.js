// Initialize the configuration server replica set
// - _id: name of the replSet
// - configsvr: marks it as a config server
// - members: the hosts in this replica set
rs.initiate({
  _id: "configReplSet",       // Replica set name for config servers
  configsvr: true,            // Enable config server mode
  members: [
    { _id: 0, host: "configsvr:27019" }  // Single member at configsvr:27019
  ]
});

// Initialize the first shard replica set
// - Each shard runs as its own replica set for redundancy
rs.initiate({
  _id: "shard1ReplSet",      // Replica set name for shard1
  members: [
    { _id: 0, host: "shard1:27018" }     // Single member at shard1:27018
  ]
});

// Initialize the second shard replica set
rs.initiate({
  _id: "shard2ReplSet",      // Replica set name for shard2
  members: [
    { _id: 0, host: "shard2:27018" }     // Single member at shard2:27018
  ]
});

// Configure the mongos router to include our shards
// - sh.addShard accepts "<replSetName>/<host>:<port>"
sh.addShard("shard1ReplSet/shard1:27018");  // Add shard1 to the sharded cluster
sh.addShard("shard2ReplSet/shard2:27018");  // Add shard2 to the sharded cluster

// Enable sharding on the 'tracker' database
// This allows collections within 'tracker' to be distributed across shards
sh.enableSharding("tracker");

// Shard the 'products' collection within the 'tracker' database
// - Key: url field hashed for even distribution
sh.shardCollection(
  "tracker.products",      // Namespace: <database>.<collection>
  { url: "hashed" }        // Shard key definition (hashed ensures uniform distribution)
);
