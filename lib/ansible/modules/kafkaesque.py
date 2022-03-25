#!/usr/bin/python

from ast import Delete
from email.policy import default
from re import IGNORECASE
from unittest import result
from venv import create
from ansible.module_utils.basic import *
from ansible.module_utils.basic import AnsibleModule
import os
import subprocess



def main():

    # Set variables as global for cross-function accessability
    global module, create, delete, describe

    module_args = dict(
        custom_bin_path                             =dict(type='str', default='kafka-topics'),
        create                                      =dict(type='bool', default=False),
        delete                                      =dict(type='bool', default=False),
        describe                                    =dict(type='bool', default=False),
        topic_name                                  =dict(type='str', required=True),
        port                                        =dict(type='str', required=True),
        bootstrap_server                            =dict(type='str', required=True),
        command_config                              =dict(type='str'),
        cleanup_policy                              =dict(type='str'),
        confluent_key_schema_validation             =dict(type='str'),
        confluent_key_subject_name_strategy         =dict(type='str'),
        confluent_tier_enable                       =dict(type='str'),
        confluent_tier_local_hotset_bytes           =dict(type='str'),
        confluent_value_schema_validation           =dict(type='str'),
        confluent_value_subject_name_strategy       =dict(type='str'),
        delete_retention_ms                         =dict(type='str'),
        file_delete_ms                              =dict(type='str'),
        flush_ms                                    =dict(type='str'),
        follower_replication_throttled_replicas     =dict(type='str'),
        index_interval_bytes                        =dict(type='str'),
        leader_replication_throttled_replicas       =dict(type='str'),
        max_compaction_lag_ms                       =dict(type='str'),
        max_message_bytes                           =dict(type='str'),
        message_timestamp_type                      =dict(type='str'),
        min_cleanable_dirty_ratio                   =dict(type='str'),
        min_compaction_lag_ms                       =dict(type='str'),
        min_insync_replicas                         =dict(type='str'),
        preallocate                                 =dict(type='str'),
        retention_bytes                             =dict(type='str'),
        segment_bytes                               =dict(type='str'),
        segment_index_bytes                         =dict(type='str'),
        segment_jitter_ms                           =dict(type='str'),
        segment_ms                                  =dict(type='str'),
        unclean_leader_election_enable              =dict(type='str'),
        confluent_placement_constraints             =dict(type='str'),
        message_downconversion_enable               =dict(type='str')
    )

    # Store variables
    module          = AnsibleModule(argument_spec=module_args)
    create          = module.params['create']
    delete          = module.params['delete']
    describe        = module.params['describe']

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    
    # Validate that an action has been selected (Create, Delete og Describe), as well as validate that not more than one is selected
    validate_action_input()
    
    # Create string containing kafka-topics path as well as flag related to action
    create_action_string()
    
    # Add remaining required parameters
    append_remaining_required_params()


    module.exit_json(changed=True, meta=module.params)

def validate_action_input():
    if create == True and delete == True and describe == False:
        module.fail_json(msg='Both create and delete cannot be True at the same time.')
    else: pass

    if create == True and describe == True and delete == False:
        module.fail_json(msg='Both create and describe cannot be True at the same time.')
    else: pass
    
    if delete == True and describe == True and create == False:
        module.fail_json(msg='Both describe and delete cannot be True at the same time.')
    else: pass

    if create == True and delete == True and describe == True:
        module.fail_json(msg='Create, describe and delete cannot be True at the same time.')
    else: pass

    if create == False and delete == False and describe == False:
        module.fail_json(msg='Create, describe or delete must be set True.')
    else: pass

def create_action_string():
    if create == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --create "})
    elif delete == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --delete "})
    elif describe == True:
        module.params.update({"action": module.params['custom_bin_path'] + " --describe "})
    else: module.fail_json(msg='Should not be reached')

def append_remaining_required_params():

    module.params.update({"action_with_required": \
                            module.params['action'] + \
                            module.params['bootstrap_server'] + \
                            ':' + \
                            module.params['port'] + ' --topic ' + \
                            module.params['topic_name'] \
    })
    

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
