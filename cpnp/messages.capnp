@0xce11dae8cd4b9326;

struct AttestationRecord {
    slot @0 :UInt64 = 0;
    shardId @1 :UInt16 = 0;
    obliqueParentHashes @2 :List(Data) = [];
    shardBlockHash @3 :Data = 0x"00";
    attesterBitfield @4 :Data = "";
    aggregateSig @5 :List(Data) = [0x"00", 0x"00"];
}


struct Block {
    parentHash @0 :Data = 0x"00";
    slotNumber @1 :UInt64 = 0;
    randaoReveal @2 :Data = 0x"00";
    attestations @3 :List(AttestationRecord) = [];
    powChainRef @4 :Data = 0x"00";
    activateStateRoot @5 :Data = 0x"00";
    crystallizedStateRoot @6 :Data = 0x"00";
}

struct ShardAndCommittee {
    shardId @0 :UInt16 = 0;
    # Note: Restrict committee to INT24 detailed in specification;
    committee @1 :List(UInt32) = [];
}

struct CrosslinkRecord {
    dynasty @0 :UInt64 = 0;
    hash @1 :Data = 0x"00";
}

struct ValidatorRecord {
    pubkey @0 :Data = 0x"00";
    withdrawalShard @1 :UInt16 = 0;
    withdrawalAddress @2 :Data = 0x"00";
    randaoCommitment @3 :Data = 0x"00";
    balance @4 :UInt64 = 0;
    startDynasty @5 :UInt64 = 0;
    endDynasty @6 :UInt64 = 0;
}

struct CrystallizedState {
    validators @0 :List(ValidatorRecord) = [];
    lastStateRecalc @1 :UInt64 = 0;
    indicesForSlots @2 :List(List(ShardAndCommittee)) = [];
    lastJustifiedSlot @3 :UInt64 = 0;
    jutifiedStreak @4 :UInt64 = 0;
    lastFinalizedSlot @5 :UInt64 = 0;
    currentDynasty @6 :UInt64 = 0;
    crosslinkingStartShard @7 :UInt16 = 0;
    crosslinkRecords @8 :List(CrosslinkRecord) = [];
    totalDeposits @9 :Data = 0x"00";
    dynastySeed @10 :Data = 0x"00";
    dynastySeedLastReset @11 :UInt64 = 0;
}
