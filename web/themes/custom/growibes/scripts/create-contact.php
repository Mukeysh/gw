<?php

/**
 * Create or update the Growibes contact Webform.
 *
 * Run: ddev drush php:script web/themes/custom/growibes/scripts/create-contact.php
 */

use Drupal\webform\Entity\Webform;

$elements = <<<'YAML'
name:
  '#type': textfield
  '#title': Your name
  '#attributes':
    autocomplete: name
  '#wrapper_attributes':
    class:
      - gw-field
company:
  '#type': textfield
  '#title': Company
  '#attributes':
    autocomplete: organization
  '#wrapper_attributes':
    class:
      - gw-field
email:
  '#type': email
  '#title': Work email
  '#required': true
  '#attributes':
    autocomplete: email
  '#wrapper_attributes':
    class:
      - gw-field
role:
  '#type': textfield
  '#title': Your role
  '#attributes':
    autocomplete: organization-title
  '#wrapper_attributes':
    class:
      - gw-field
need:
  '#type': radios
  '#title': What brings you here?
  '#options':
    'Platform modernization': Platform modernization
    'Enterprise Drupal': Enterprise Drupal
    'AI engineering': AI engineering
    'Architecture / roadmap': Architecture / roadmap
    'Connected systems': Connected systems
    'Agency partnership': Agency partnership
    'Free 14-day sprint': Free 14-day sprint
  '#wrapper_attributes':
    class:
      - gw-field
      - gw-field--full
      - gw-choices
message:
  '#type': textarea
  '#title': What is changing, stuck or at risk?
  '#placeholder': 'A few sentences are enough. What are you trying to achieve, what is getting in the way, and what cannot break?'
  '#description': 'Please do not include passwords, API keys, payment details, health information or other sensitive credentials.'
  '#wrapper_attributes':
    class:
      - gw-field
      - gw-field--full
timeline:
  '#type': select
  '#title': When does this matter?
  '#empty_option': 'Not sure yet'
  '#options':
    Immediately: Immediately
    'Within 30 days': Within 30 days
    '1–3 months': 1–3 months
    '3–6 months': 3–6 months
    '6+ months': 6+ months
  '#wrapper_attributes':
    class:
      - gw-field
source:
  '#type': select
  '#title': How did you find us?
  '#empty_option': 'Select one'
  '#options':
    Search: Search
    Referral: Referral
    LinkedIn: LinkedIn
    'Drupal community': Drupal community
    'Existing relationship': Existing relationship
    Other: Other
  '#wrapper_attributes':
    class:
      - gw-field
privacy_note:
  '#type': webform_markup
  '#markup': '<p class="form-note">By submitting, your email may be used to respond to this enquiry as described in our <a href="/privacy" rel="noopener">Privacy Notice</a>. No marketing consent is implied.</p>'
  '#wrapper_attributes':
    class:
      - gw-field
      - gw-field--full
marketing:
  '#type': checkbox
  '#title': 'Yes, I would like occasional Growibes insights, updates and relevant offers. <b>This is optional.</b>'
  '#title_display': after
  '#wrapper_attributes':
    class:
      - gw-field
      - gw-field--full
      - gw-consent
actions:
  '#type': webform_actions
  '#title': Submit
  '#submit__label': 'Send to Growibes →'
YAML;

$settings = Webform::getDefaultSettings();
$settings['page'] = TRUE;
$settings['page_submit_path'] = '/contact';
$settings['form_title'] = 'none';
$settings['form_open_message'] = '';
$settings['form_exception_message'] = '';
$settings['form_attributes'] = [
  'class' => ['gw-contact-form'],
];
$settings['confirmation_type'] = 'inline';
$settings['confirmation_title'] = '';
$settings['confirmation_message'] = '<p class="gw-contact-thanks"><strong>Thank you.</strong> We have your enquiry and will route it to the right senior people. This is not a marketing subscription.</p>';
$settings['form_submit_once'] = TRUE;
$settings['form_novalidate'] = FALSE;
$settings['form_required'] = FALSE;
$settings['token_update'] = FALSE;

$webform = Webform::load('growibes_contact');
if (!$webform) {
  $webform = Webform::create([
    'id' => 'growibes_contact',
    'title' => 'Contact Growibes',
    'description' => 'Growibes enterprise contact / start a conversation.',
    'status' => TRUE,
    'uid' => 1,
  ]);
}

$webform->set('elements', $elements);
$webform->set('settings', $settings);
$webform->set('handlers', [
  'email_nitish' => [
    'id' => 'email',
    'label' => 'Email Growibes',
    'handler_id' => 'email_nitish',
    'status' => TRUE,
    'weight' => 0,
    'settings' => [
      'states' => ['completed'],
      'to_mail' => 'nitish@growibes.com',
      'cc_mail' => 'hello@growibes.com',
      'from_mail' => '_default',
      'from_name' => 'Growibes website',
      'subject' => 'Growibes contact: [webform_submission:values:need:raw] ([webform_submission:values:email:raw])',
      'body' => '_default',
      'html' => TRUE,
      'exclude_empty' => TRUE,
      'ignore_access' => FALSE,
      'attachments' => FALSE,
      'twig' => FALSE,
      'debug' => FALSE,
      'to_options' => [],
      'cc_options' => [],
      'bcc_mail' => '',
      'bcc_options' => [],
      'from_options' => [],
      'reply_to' => '[webform_submission:values:email:raw]',
      'return_path' => '',
      'sender_mail' => '',
      'sender_name' => '',
      'theme_name' => '',
      'parameters' => [],
      'excluded_elements' => [],
    ],
  ],
]);
$webform->setAccessRules([
  'create' => [
    'roles' => ['anonymous', 'authenticated'],
    'users' => [],
    'permissions' => [],
  ],
  'view_any' => [
    'roles' => ['administrator'],
    'users' => [],
    'permissions' => [],
  ],
]);
$webform->save();

echo 'Webform growibes_contact saved. url=/contact id=', $webform->id(), PHP_EOL;
