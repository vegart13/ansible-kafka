#!/usr/bin/python

from ast import Delete
from email.policy import default
from re import IGNORECASE
from ssl import AlertDescription
from unittest import result
from venv import create
from ansible.module_utils.basic import *
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess



def main():

    # Set variables as global for cross-function accessability
    global module, optionallist, action_bool_list, create, delete, describe, alter, command_config, cleanup_policy

    module_args = dict(
        custom_bin_path                             =dict(type='str', default='kafka-topics'),
        create                                      =dict(type='bool', default=False),
        delete                                      =dict(type='bool', default=False),
        describe                                    =dict(type='bool', default=False),
        alter                                       =dict(type='bool', default=False),
        topic_name                                  =dict(type='str', required=True),
        port                                        =dict(type='str', required=True),
        bootstrap_server                            =dict(type='str', required=True),
        command_config                              =dict(type='str', default='undefined'),
        cleanup_policy                              =dict(type='str', default='undefined'),
        compression_type                            =dict(type='str', default='undefined'),
        confluent_key_schema_validation             =dict(type='str', default='undefined'),
        confluent_key_subject_name_strategy         =dict(type='str', default='undefined'),
        confluent_tier_enable                       =dict(type='str', default='undefined'),
        confluent_tier_local_hotset_bytes           =dict(type='str', default='undefined'),
        confluent_value_schema_validation           =dict(type='str', default='undefined'),
        confluent_value_subject_name_strategy       =dict(type='str', default='undefined'),
        delete_retention_ms                         =dict(type='str', default='undefined'),
        file_delete_ms                              =dict(type='str', default='undefined'),
        flush_ms                                    =dict(type='str', default='undefined'),
        follower_replication_throttled_replicas     =dict(type='str', default='undefined'),
        index_interval_bytes                        =dict(type='str', default='undefined'),
        leader_replication_throttled_replicas       =dict(type='str', default='undefined'),
        max_compaction_lag_ms                       =dict(type='str', default='undefined'),
        max_message_bytes                           =dict(type='str', default='undefined'),
        message_timestamp_difference_max_ms         =dict(type='str', default='undefined'),
        message_timestamp_type                      =dict(type='str', default='undefined'),
        min_cleanable_dirty_ratio                   =dict(type='str', default='undefined'),
        min_compaction_lag_ms                       =dict(type='str', default='undefined'),
        min_insync_replicas                         =dict(type='str', default='undefined'),
        preallocate                                 =dict(type='str', default='undefined'),
        retention_bytes                             =dict(type='str', default='undefined'),
        segment_bytes                               =dict(type='str', default='undefined'),
        segment_index_bytes                         =dict(type='str', default='undefined'),
        segment_jitter_ms                           =dict(type='str', default='undefined'),
        segment_ms                                  =dict(type='str', default='undefined'),
        unclean_leader_election_enable              =dict(type='str', default='undefined'),
        confluent_placement_constraints             =dict(type='str', default='undefined'),
        message_downconversion_enable               =dict(type='str', default='undefined')
    )

    # Store variables
    module                                          = AnsibleModule(argument_spec=module_args)
    optionallist                                    = list()
    action_bool_list                                = list()
    create                                          = module.params['create']
    delete                                          = module.params['delete']
    describe                                        = module.params['describe']
    alter                                           = module.params['alter']
    command_config                                  = ' --command-config ' +  module.params['command_config']
    cleanup_policy                                  = ' --config cleanup.policy=' + module.params['cleanup_policy']
    compression_type                                = ' --config compression.type=' + module.params['compression_type']
    confluent_key_schema_validation                 = ' --config confluent.key.schema.validation=' + module.params['confluent_key_schema_validation']
    confluent_key_subject_name_strategy             = ' --config confluent.key.subject.name.strategy=' + module.params['confluent_key_subject_name_strategy']
    confluent_tier_enable                           = ' --config confluent.tier.enable=' + module.params['confluent_tier_enable']
    confluent_tier_local_hotset_bytes               = ' --config confluent.tier.local.hotset.bytes=' + module.params['confluent_tier_local_hotset_bytes']
    confluent_value_schema_validation               = ' --config confluent.value.schema.validation=' + module.params['confluent_value_schema_validation']
    confluent_value_subject_name_strategy           = ' --config confluent.value.subject.name.strategy=' + module.params['confluent_value_subject_name_strategy']
    delete_retention_ms                             = ' --config delete.retention.ms=' + module.params['delete_retention_ms']
    file_delete_ms                                  = ' --config file.delete.ms=' + module.params['file_delete_ms']
    flush_ms                                        = ' --config flush.ms=' + module.params['flush_ms']
    follower_replication_throttled_replicas         = ' --config follower.replication.throttled.replicas=' + module.params['follower_replication_throttled_replicas']
    index_interval_bytes                            = ' --config index.interval.bytes=' + module.params['index_interval_bytes']
    leader_replication_throttled_replicas           = ' --config leader.replication.throttled.replicas=' + module.params['leader_replication_throttled_replicas']
    max_compaction_lag_ms                           = ' --config max.compaction.lag.ms=' + module.params['max_compaction_lag_ms']
    max_message_bytes                               = ' --config max.message.bytes=' + module.params['max_message_bytes']
    message_timestamp_difference_max_ms             = ' --config message.timestamp.difference.max.ms=' + module.params['message_timestamp_difference_max_ms']
    min_cleanable_dirty_ratio                       = ' --config min.cleanable.dirty.ratio=' + module.params['min_cleanable_dirty_ratio']
    min_compaction_lag_ms                           = ' --config min.compaction.lag.ms=' + module.params['min_compaction_lag_ms']
    min_insync_replicas                             = ' --config min.insync.replicas=' + module.params['min_insync_replicas']
    preallocate                                     = ' --config preallocate=' + module.params['preallocate']
    segment_bytes                                   = ' --config segment.bytes=' + module.params['segment_bytes']
    segment_index_bytes                             = ' --config segment.index.bytes=' + module.params['segment_index_bytes']
    segment_jitter_ms                               = ' --config segment.jitter.ms=' + module.params['segment_jitter_ms']
    segment_ms                                      = ' --config segment.ms=' + module.params['segment_ms']
    unclean_leader_election_enable                  = ' --config unclean.leader.election.enable=' + module.params['unclean_leader_election_enable']
    confluent_placement_constraints                 = ' --config confluent.placement.constraints=' + module.params['confluent_placement_constraints']
    message_downconversion_enable                   = ' --config message.downconversion.enable=' + module.params['message_downconversion_enable']

    # 1. Validate that an action has been selected (Create, Delete og Describe), as well as validate that not more than one is selected
    validate_action_input()
    
    # 2. Create string containing kafka-topics path as well as flag related to action
    create_action_string()
    
    # 3. Add remaining required parameters
    append_remaining_required_params()

    # 4. Add defined optional parameters to list
    add_defined_optional_to_list()
    
    # 5. Concatenate items in list to string
    concatenated_sentence = ' '.join(optionallist)


    complete_string = module.params['action'] + concatenated_sentence

    module.params.update({"complete": complete_string})


    # Ansible exit
    module.exit_json(changed=True, meta=module.params)

def validate_action_input():
    action_bool_list = [module.params['create'], module.params['delete'], module.params['describe'], module.params['alter']]
    if sum(action_bool_list) > 1:
        module.fail_json(msg='Only one action can be chosen at the same time. (Create, Delete, Descibe, Alter')
    else: pass

def create_action_string():
    if create == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --create "})
    elif delete == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --delete "})
    elif describe == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --describe "})
    elif alter == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --alter "})
    else: module.fail_json(msg='Should not be reached')

def append_remaining_required_params():
    module.params.update({"action_with_required": \
                            module.params['action'] + \
                            module.params['bootstrap_server'] + \
                            ':' + \
                            module.params['port'] + \
                            ' --topic ' + \
                            module.params['topic_name'] \
    })

def add_defined_optional_to_list():
    if module.params['command_config'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['cleanup_policy'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['compression_type'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['confluent_key_schema_validation'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['confluent_key_subject_name_strategy'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['confluent_tier_enable'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['confluent_tier_local_hotset_bytes'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['confluent_value_schema_validation'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['confluent_value_subject_name_strategy'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['delete_retention_ms'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['file_delete_ms'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['flush_ms'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['follower_replication_throttled_replicas'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['index_interval_bytes'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['leader_replication_throttled_replicas'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['max_compaction_lag_ms'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['max_message_bytes'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['message_timestamp_difference_max_ms'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['message_timestamp_type'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['min_cleanable_dirty_ratio'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['min_compaction_lag_ms'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['min_insync_replicas'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['preallocate'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['retention_bytes'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['segment_bytes'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['segment_index_bytes'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['segment_jitter_ms'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['segment_ms'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['unclean_leader_election_enable'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['min_cleanable_dirty_ratio'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    if module.params['confluent_placement_constraints'] != 'undefined':
        optionallist.append(command_config)
    else: pass

    if module.params['message_downconversion_enable'] != 'undefined':
        optionallist.append(cleanup_policy)
    else: pass

    module.params.update({"list": optionallist})

    # Save command to param then convert to string
    # kafka.params.update({"test": required_string})
    # shellscript = str(kafka.params["test"])

    # Execute string on system
    #os.system(shellscript)

    # Exit
    #module.exit_json(changed=True, meta=module.params)
    # kafka.exit_json(changed=True, meta=kafka.params)

if __name__ == '__main__':
    main()
