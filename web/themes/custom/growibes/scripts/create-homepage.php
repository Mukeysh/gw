<?php

/**
 * Creates/updates the Growibes homepage as a Canvas page using growibes:html.
 *
 * Run: ddev drush php:script web/themes/custom/growibes/scripts/create-homepage.php
 */

use Drupal\canvas\Entity\Component;
use Drupal\canvas\Entity\Page;
use Drupal\Core\Url;

$theme_path = \Drupal::service('extension.list.theme')->getPath('growibes');
$html = file_get_contents($theme_path . '/components/html/examples/homepage.html');
$css = file_get_contents($theme_path . '/components/html/examples/homepage.css');
if ($html === FALSE || $css === FALSE) {
  throw new \RuntimeException('Missing homepage example HTML/CSS in the Growibes theme.');
}

$component = Component::load('sdc.growibes.html');
if (!$component) {
  throw new \RuntimeException('Canvas component sdc.growibes.html is missing. Enable the Growibes theme and clear caches.');
}

$uuid = \Drupal::service('uuid')->generate();
$tree = [
  [
    'uuid' => $uuid,
    'component_id' => 'sdc.growibes.html',
    'component_version' => $component->getActiveVersion(),
    'inputs' => [
      'html' => $html,
      'css' => $css,
    ],
  ],
];

$storage = \Drupal::entityTypeManager()->getStorage('canvas_page');
$existing = $storage->loadByProperties(['title' => 'Home']);
$page = $existing ? reset($existing) : Page::create([
  'title' => 'Home',
  'status' => TRUE,
]);
$page->set('title', 'Home');
$page->set('status', TRUE);
$page->set('path', ['alias' => '/home']);
$page->set('description', 'Growibes — Enterprise Digital Engineering for the Drupal + AI Era');
if (method_exists($page, 'setOwnerId')) {
  $page->setOwnerId(1);
}
$page->setComponentTree($tree);

$violations = $page->validate();
if ($violations->count()) {
  foreach ($violations as $violation) {
    echo $violation->getPropertyPath(), ': ', $violation->getMessage(), PHP_EOL;
  }
  throw new \RuntimeException('Homepage Canvas page failed validation.');
}

$page->save();

\Drupal::configFactory()->getEditable('system.site')
  ->set('page.front', '/home')
  ->set('name', 'Growibes')
  ->save();

$url = Url::fromRoute('entity.canvas_page.canonical', ['canvas_page' => $page->id()], ['absolute' => TRUE])->toString();
echo "Homepage canvas page {$page->id()} saved.\n";
echo "Alias: /home\n";
echo "Canonical: {$url}\n";
echo "HTML bytes: " . strlen($html) . " CSS bytes: " . strlen($css) . "\n";
