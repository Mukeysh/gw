<?php

declare(strict_types=1);

namespace Drupal\growibes_canvas\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\HttpKernel\KernelEvents;

/**
 * 301 old Growibes aliases onto the capabilities IA tree.
 */
final class AliasRedirectSubscriber implements EventSubscriberInterface {

  private const MAP = [
    '/digital-platforms' => '/capabilities/digital-platforms',
    '/digital-platforms/enterprise-drupal' => '/capabilities/digital-platforms/enterprise-drupal',
    '/digital-platforms/migrations' => '/capabilities/digital-platforms/migration-modernization',
    '/digital-platforms/multisite' => '/capabilities/digital-platforms/multisite-multibrand',
    '/digital-platforms/multilingual' => '/capabilities/digital-platforms/global-multilingual',
    '/digital-platforms/content-governance' => '/capabilities/digital-platforms/content-governance',
    '/digital-platforms/digital-asset-management' => '/capabilities/digital-platforms/digital-asset-management',
    '/experience/seo-aeo' => '/capabilities/experience-growth/seo-aeo-ai-visibility',
    '/experience/marketing-automation' => '/capabilities/experience-growth/marketing-automation',
    '/experience/design-systems' => '/capabilities/experience-growth/design-systems',
    '/experience/personalization' => '/capabilities/experience-growth/personalization',
    '/experience/analytics' => '/capabilities/experience-growth/analytics-optimization',
    '/experience/commerce' => '/capabilities/experience-growth/commerce',
    '/intelligent-enterprise' => '/capabilities/intelligent-enterprise',
    '/intelligent-enterprise/ai' => '/capabilities/intelligent-enterprise/ai-agents',
    '/intelligent-enterprise/drupal-ai' => '/capabilities/intelligent-enterprise/drupal-ai',
    '/intelligent-enterprise/sovereign-core' => '/capabilities/intelligent-enterprise/sovereign-core',
    '/connected-enterprise' => '/capabilities/connected-enterprise',
    '/connected-enterprise/apis' => '/capabilities/connected-enterprise/composable',
    '/connected-enterprise/integrations' => '/capabilities/connected-enterprise/integrations',
    '/connected-enterprise/headless' => '/capabilities/connected-enterprise/headless-api-first',
    '/engineering/digital-trust' => '/capabilities/enterprise-engineering/security',
    '/engineering/security-performance' => '/capabilities/enterprise-engineering/performance',
    '/engineering/cloud-devops' => '/capabilities/enterprise-engineering/cloud-devops',
    '/engineering/continuous-engineering' => '/capabilities/enterprise-engineering/continuous-engineering',
    '/agencies' => '/agency-partnerships',
    '/work/sph' => '/work/singapore-press-holdings',
    '/work/ibp' => '/work/international-budget-partnership',
    '/work/confidential-enterprise' => '/work/confidential-enterprise-platform',
    '/our-story' => '/why-growibes/himalayan-story',
  ];

  public static function getSubscribedEvents(): array {
    return [KernelEvents::REQUEST => ['onRequest', 30]];
  }

  public function onRequest(RequestEvent $event): void {
    if (!$event->isMainRequest()) {
      return;
    }
    $path = rtrim($event->getRequest()->getPathInfo(), '/') ?: '/';
    if (!isset(self::MAP[$path])) {
      return;
    }
    $event->setResponse(new RedirectResponse(self::MAP[$path], 301));
  }

}
