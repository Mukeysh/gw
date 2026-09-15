<?php

/**
 * Rebuild the Drupal Main navigation to match the Growibes IA tree.
 *
 * Run: ddev drush php:script web/themes/custom/growibes/scripts/create-menu.php
 */

use Drupal\menu_link_content\Entity\MenuLinkContent;

$storage = \Drupal::entityTypeManager()->getStorage('menu_link_content');
foreach ($storage->loadByProperties(['menu_name' => 'main']) as $link) {
  $link->delete();
}
\Drupal::service('plugin.manager.menu.link')->updateDefinition('standard.front_page', ['enabled' => FALSE]);

$weight = 0;
$nolink = 'route:<nolink>';

$add = function (string $title, string $uri, ?MenuLinkContent $parent = NULL, bool $expanded = TRUE) use (&$weight, $storage): MenuLinkContent {
  $link = $storage->create([
    'title' => $title,
    'link' => ['uri' => $uri],
    'menu_name' => 'main',
    'expanded' => $expanded,
    'enabled' => TRUE,
    'weight' => $weight++,
  ]);
  if ($parent) {
    $link->set('parent', 'menu_link_content:' . $parent->uuid());
  }
  $link->save();
  return $link;
};

$capabilities = $add('Capabilities', $nolink);

$digital = $add('Digital Platforms', $nolink, $capabilities);
$add('Overview', 'internal:/capabilities/digital-platforms', $digital);
foreach ([
  'Enterprise Drupal' => '/capabilities/digital-platforms/enterprise-drupal',
  'Migration & Modernization' => '/capabilities/digital-platforms/migration-modernization',
  'Multisite & Multi-brand' => '/capabilities/digital-platforms/multisite-multibrand',
  'Global & Multilingual' => '/capabilities/digital-platforms/global-multilingual',
  'Content Governance' => '/capabilities/digital-platforms/content-governance',
  'Digital Asset Management' => '/capabilities/digital-platforms/digital-asset-management',
] as $title => $path) {
  $add($title, 'internal:' . $path, $digital);
}

$experience = $add('Experience & Growth', $nolink, $capabilities);
foreach ([
  'Personalization' => '/capabilities/experience-growth/personalization',
  'Analytics & Optimization' => '/capabilities/experience-growth/analytics-optimization',
  'Commerce' => '/capabilities/experience-growth/commerce',
  'SEO, AEO & AI Visibility' => '/capabilities/experience-growth/seo-aeo-ai-visibility',
  'Marketing Automation' => '/capabilities/experience-growth/marketing-automation',
  'Design Systems' => '/capabilities/experience-growth/design-systems',
] as $title => $path) {
  $add($title, 'internal:' . $path, $experience);
}

$intelligent = $add('Intelligent Enterprise', $nolink, $capabilities);
$add('Overview', 'internal:/capabilities/intelligent-enterprise', $intelligent);
foreach ([
  'Drupal AI' => '/capabilities/intelligent-enterprise/drupal-ai',
  'AI Agents' => '/capabilities/intelligent-enterprise/ai-agents',
  'Enterprise Search' => '/',
  'Sovereign CORE' => '/capabilities/intelligent-enterprise/sovereign-core',
] as $title => $path) {
  $add($title, 'internal:' . $path, $intelligent);
}

$connected = $add('Connected Enterprise', $nolink, $capabilities);
$add('Overview', 'internal:/capabilities/connected-enterprise', $connected);
foreach ([
  'Integrations' => '/capabilities/connected-enterprise/integrations',
  'Headless / API-first' => '/capabilities/connected-enterprise/headless-api-first',
  'Enterprise Data' => '/',
  'Composable' => '/capabilities/connected-enterprise/composable',
] as $title => $path) {
  $add($title, 'internal:' . $path, $connected);
}

$engineering = $add('Enterprise Engineering', $nolink, $capabilities);
foreach ([
  'Security' => '/capabilities/enterprise-engineering/security',
  'Performance' => '/capabilities/enterprise-engineering/performance',
  'Accessibility' => '/',
  'Cloud & DevOps' => '/capabilities/enterprise-engineering/cloud-devops',
  'Continuous Engineering' => '/capabilities/enterprise-engineering/continuous-engineering',
] as $title => $path) {
  $add($title, 'internal:' . $path, $engineering);
}

$strategy = $add('Strategy', $nolink);
$add('Overview', 'internal:/strategy', $strategy);
foreach ([
  'Digital Strategy' => '/',
  'Enterprise Architecture' => '/strategy/enterprise-architecture',
  'Platform Roadmaps' => '/',
  'Technical Discovery' => '/strategy/technical-discovery',
] as $title => $path) {
  $add($title, 'internal:' . $path, $strategy);
}

$work = $add('Work', $nolink);
$add('Overview', 'internal:/work', $work);
foreach ([
  'WSO2' => '/work/wso2',
  'Singapore Press Holdings' => '/work/singapore-press-holdings',
  'Fosroc' => '/work/fosroc',
  'International Budget Partnership' => '/work/international-budget-partnership',
  'Confidential Enterprise Platform' => '/work/confidential-enterprise-platform',
] as $title => $path) {
  $add($title, 'internal:' . $path, $work);
}

$add('Agencies', 'internal:/agency-partnerships');

$why = $add('Why Growibes', $nolink);
$add('Himalayan Story', 'internal:/why-growibes/himalayan-story', $why);

$start = $add('Start', $nolink);
$add('Contact', 'internal:/contact', $start);
$add('Free 14-day sprint', 'internal:/strategy/technical-discovery', $start);

echo "Main menu rebuilt.\n";
