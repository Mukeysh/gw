<?php

/**
 * Create Canvas pages from extracted HTML/CSS examples.
 *
 * Run:
 *   ddev drush php:script web/themes/custom/growibes/scripts/create-pages.php digital-platforms
 *   ddev drush php:script web/themes/custom/growibes/scripts/create-pages.php all
 */

use Drupal\canvas\Entity\Component;
use Drupal\canvas\Entity\Page;

$group = $extra[0] ?? 'digital-platforms';
$filters = array_values(array_filter(array_map('trim', explode(',', $group))));

$theme_path = \Drupal::service('extension.list.theme')->getPath('growibes');
$catalog_path = $theme_path . '/scripts/pages.json';
$examples = $theme_path . '/components/html/examples';
$pages = json_decode(file_get_contents($catalog_path), TRUE, 512, JSON_THROW_ON_ERROR);

$component = Component::load('sdc.growibes.html');
if (!$component) {
  throw new \RuntimeException('Canvas component sdc.growibes.html is missing.');
}

$storage = \Drupal::entityTypeManager()->getStorage('canvas_page');
$existing_by_title = [];
$existing_by_alias = [];
foreach ($storage->loadMultiple() as $existing) {
  $existing_by_title[$existing->label()] = $existing;
  $alias = (string) $existing->get('path')->alias;
  if ($alias !== '') {
    $existing_by_alias[$alias] = $existing;
  }
}

$uuid = \Drupal::service('uuid');
$created = 0;
$updated = 0;

foreach ($pages as $spec) {
  if ($group !== 'all') {
    $match = in_array($spec['slug'], $filters, TRUE) || in_array($spec['group'], $filters, TRUE);
    if (count($filters) > 1) {
      $match = in_array($spec['slug'], $filters, TRUE);
    }
    if (!$match) {
      continue;
    }
  }

  $html_file = $examples . '/' . $spec['slug'] . '.html';
  $css_file = $examples . '/' . $spec['slug'] . '.css';
  if (!is_readable($html_file) || !is_readable($css_file)) {
    echo "SKIP missing extract {$spec['slug']}\n";
    continue;
  }

  $html = file_get_contents($html_file);
  $css = file_get_contents($css_file);
  $tree = [
    [
      'uuid' => $uuid->generate(),
      'component_id' => 'sdc.growibes.html',
      'component_version' => $component->getActiveVersion(),
      'inputs' => [
        'html' => $html,
        'css' => $css,
      ],
    ],
  ];

  $page = $existing_by_title[$spec['title']]
    ?? $existing_by_alias[$spec['alias']]
    ?? Page::create([
      'title' => $spec['title'],
      'status' => TRUE,
    ]);
  $is_new = $page->isNew();
  $page->set('title', $spec['title']);
  $page->set('status', TRUE);
  $page->set('path', ['alias' => $spec['alias']]);
  $page->set('description', $spec['title'] . ' — Growibes');
  if (method_exists($page, 'setOwnerId')) {
    $page->setOwnerId(1);
  }
  $page->setComponentTree($tree);

  $violations = $page->validate();
  if ($violations->count()) {
    echo "FAIL {$spec['alias']}\n";
    foreach ($violations as $violation) {
      echo '  ', $violation->getPropertyPath(), ': ', $violation->getMessage(), PHP_EOL;
    }
    continue;
  }

  $page->save();
  $existing_by_alias[$spec['alias']] = $page;
  $is_new ? $created++ : $updated++;
  echo ($is_new ? 'CREATE' : 'UPDATE'), " {$page->id()} {$spec['alias']} html=", strlen($html), " css=", strlen($css), PHP_EOL;
}

echo "done group={$group} created={$created} updated={$updated}\n";
