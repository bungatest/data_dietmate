import { RecipeDetailScreen } from "@/components/recipes/recipe-detail-screen";

export default function RecipePage({
  params
}: {
  params: { id: string };
}) {
  return <RecipeDetailScreen recipeId={params.id} />;
}
